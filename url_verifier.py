import streamlit as st
from pathlib import Path
from io import StringIO
import sqlite3
from sqlite3 import Error
import time
import string
import random



def main():
    st.set_page_config(
        page_title='URL verifier',
        page_icon='✅'
        )
    st.title( 'URL verifier' )

    # NOTE: Query contents of database
    db_fullpath = clean_path( 'app_db.sqlite3' )
    references = query_all_tables( db_fullpath )
    
    # NOTE: START single link verification widgets
    url = st.text_input( 'URL' )
    url_submitted = st.button( 'Verify URL' )

    if url_submitted:
        if not url:
            st.error( 'Please provide a URL as input.' )
        else:
            render_progress( url )
            evaluate( url, references, True )
    # NOTE: END single link verification widgets
    
    # NOTE: START multiple link verification widgets
    url_list = st.file_uploader(
        'Text file containing URLs to verify:',
        type='txt',
        accept_multiple_files=False
        )
    list_submitted = st.button( 'Verify URLs in list' )

    if list_submitted:
        if url_list is None:
            st.error( 'Please select a file containing URLs to verify.' )
        else:
            list_contents = read_file_contents( url_list )

            if not list_contents:
                st.error( 'No URLs found in the file.' )
            else:
                for url in list_contents:
                    render_progress( url )
                    evaluate( url, references )
    # NOTE: END multiple link verification widgets


def clean_path( path: str ) -> str:
    raw_path = Path( path )
    return raw_path.resolve().as_posix()


@st.cache
def query_all_tables( db_fullpath: str ) -> dict:
    tables = ['credible_refs', 'infamous_refs', 'neutral_sites']
    db_conn = None

    try:
        db_conn = sqlite3.connect( db_fullpath )
    except Error as e:
        print( f'Database connection error: {e}' )
        return

    results = dict()

    for table in tables:
        table_content = list()

        with db_conn:
            query = f'SELECT * FROM {table};'
            cursor = db_conn.cursor()
            cursor.execute( query )
            rows = cursor.fetchall()

            for row in rows:
                table_content.append( row[0].strip() )

            results[table] = table_content

    return results


def read_file_contents( uploaded_file: object ) -> list:
    bytes_data = uploaded_file.getvalue()
    stringio = StringIO( bytes_data.decode( 'utf-8' ) )
    return [entry.strip() for entry in stringio.read().split()]


def urls_have_same_hostname( input_url: str, db_url: str ) -> bool:
    input_url = input_url.lower()
    db_url = db_url.lower()

    removables = ['https://', 'http://', 'www.']

    for removable in removables:
        input_url = input_url.replace( removable, '' )
        db_url = db_url.replace( removable, '' )

    if db_url.endswith( '/' ) and not input_url.endswith( '/' ):
        input_url = f'{input_url}/'

    return db_url in input_url


def validate_url( url: str, refs: dict ) -> int:
    neutral_matches = [entry for entry in refs['neutral_sites'] if urls_have_same_hostname( url, entry )]

    if neutral_matches:
        credible_matches = [entry for entry in refs['credible_refs'] if urls_have_same_hostname( url, entry )]

        if credible_matches:
            return 0

        infamous_matches = [entry for entry in refs['infamous_refs'] if urls_have_same_hostname( url, entry )]

        if infamous_matches:
            return 1

        return 2

    else:
        credible_matches = [entry for entry in refs['credible_refs'] if urls_have_same_hostname( url, entry )]

        if credible_matches:
            return 0

        infamous_matches = [entry for entry in refs['infamous_refs'] if urls_have_same_hostname( url, entry )]

        if infamous_matches:
            return 1

        return 3


def render_progress( url: str ) -> None:
    with st.spinner( f'Scanning blockchain for data on {url} ...' ):
        prog_bar = st.progress( 0 )

        for increment in range( 100 ):
            time.sleep( 0.05 )
            prog_bar.progress( increment + 1 )


def evaluate( url: str, references: dict, show_balloons: bool=False ) -> None:
    result = validate_url( url, references )

    if result == 0:
        address = ''.join( random.choices( string.ascii_lowercase + string.digits, k=32 ) )

        st.success( f'{url} -> LEGIT 👍, entry validated in block "{address}"' )
        
        if show_balloons:
            st.balloons()

    elif result == 1:
        st.error( f'{url} -> FAKE 👎' )

    elif result == 2:
        st.info( f'{url} -> NEUTRAL 👋' )

    elif result == 3:
        st.info( f'{url} -> Not enough data for site 🤞' )
    


if __name__ == '__main__':
    main()