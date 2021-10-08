# ProteinSort
A webapp that uses data gathered from Woolworths' API to display and filter
granular information about product protein content.
<br>
Data is displayed in an infinite scroll table that can be searched and filtered by category. 
<br>
Intended for athletes, bodybuilders or anyone interested in buying high protein foods on a budget.
<br> 
<br>
Front end built using React, and React-Bootstrap. Backend using Node, Express.JS, Knex.
<br>
Data collected from Woolworths and cleaned using Python and the Requests library, then stored in an SQLite DB.
<br><br>
Run categoryRequests.py to generate the SQLite DB.
<br>
npm install and npm start in /protein-sort/ to get the front / backend going. Make sure a DB is present to get data from. 
