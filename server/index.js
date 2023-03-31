const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const app = express();

// Add mysql database connection
const db = mysql.createPool({
  host: 'mysql_db', // the host name MYSQL_DATABASE: node_mysql
  user: 'MYSQL_USER', // database user MYSQL_USER: MYSQL_USER
  password: 'MYSQL_PASSWORD', // database user password MYSQL_PASSWORD: MYSQL_PASSWORD
  database: 'project' // database name MYSQL_HOST_IP: mysql_db
})

// Enable cors security headers
app.use(cors())

// add an express method to parse the POST method
app.use(express.json())
app.use(express.urlencoded({ extended: true }));

// home page
app.get('/', (req, res) => {
  res.send('Hi There')
});

// get all of the member in the database
app.get('/get', (req, res) => {
  const SelectQuery = " SELECT * FROM  members";
  db.query(SelectQuery, (err, result) => {
    res.send(result)
  })
})

// add a member to the database
app.post("/insert", (req, res) => {
  const membersName = req.body.setName;
  const membersEmail = req.body.setEmail;
  const InsertQuery = "INSERT INTO members (name, email) VALUES (?, ?)";
  db.query(InsertQuery, [membersName, membersEmail], (err, result) => {
    console.log(result)
  })
})

// delete a member from the database
app.delete("/delete/:membersId", (req, res) => {
  const membersId = req.params.membersId;
  const DeleteQuery = "DELETE FROM members WHERE id = ?";
  db.query(DeleteQuery, membersId, (err, result) => {
    if (err) console.log(err);
  })
})

// update a member email
app.put("/update/:membersId", (req, res) => {
  const membersEmail = req.body.emailUpdate;
  const membersId = req.params.membersId;
  const UpdateQuery = "UPDATE members SET email = ? WHERE id = ?";
  db.query(UpdateQuery, [membersEmail, membersId], (err, result) => {
    if (err) console.log(err)
  })
})

app.listen('3001', () => { })