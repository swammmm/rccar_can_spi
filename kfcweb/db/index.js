// get the client
const mysql = require('mysql2/promise');

// Create the connection pool. The pool-specific settings are the defaults
const pool = mysql.createPool({
  host: '15.164.104.225',
  user: 'mincoding',
  password: "1234",
  database: 'minDB',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

module.exports = pool