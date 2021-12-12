# openit_hackathon_2021
Files we used during the Open iT Hackathon 2021 held on December 8-10, 2021 in Natura Verde Farm and Private Resort, Daet, Camarines Norte.

Event theme: `Flattening the Infodemic Curve`

Teammates: _Alvin Esquivel_, _Maica Mae Mangente_

Tools used:
* `Python 3.10.0`
* `Moon Modeler 4.3.0` - for database ER diagram creation and SQL script generation
* `DB Browser for SQLite` - for database record entry

Result: **Won 1st place**

Our output is a `Streamlit`-based prototype of a URL verifier made in Python, that determines if a provided URL or list of URLs contain legit or fake information. The concept of the backend validator is comprised of a machine learning model that scrapes through website contents to look for metadata and other relevant data to determine if the content is legit or fake, then if it is determined to be legit, the scraped data is placed in a blockchain to be used later on as reference in future validation checks.

The prototype presents the ready-to-use interface for the common user, and a simple SQLite database to crudely represent the machine learning model and the blockchain. There are two ways to provide input: a text field to contain a single URL, and a file uploader that can be used to select a text file containing a newline-separated list of URLs. Each mode of use has a separate `Verify` button. When a `Verify` button is clicked, a spinner and progress bar widget will pop up to indicate progress done on the action. When the progress bar is fully filled, the spinner widget disappears, and a message is shown below the progress bar indicating the results of the validation, which will tell if a URL's contents is either `Fake`, `Legit`, `Neutral` (base URL for sites which cannot spread fake content on their own, like `lazada.com.ph`, `twitter.com`, `fb.com`, `shopee.ph`, etc.), or `Not enough data` (site is relatively new for the machine learning model).
