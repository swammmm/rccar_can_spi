const express = require('express')
const app = express()
const port = 3000
const cors = require("cors");
const pool = require("./db");

const http = require('http')
const server = http.createServer(app)
const { Server } = require('socket.io');
const io = new Server(server, {
  cors:{
    origin: true
  },
  pingInterval: 100, //100 ms
  pingTimeout: 1
});

app.use(
    cors({
        origin: true
    })
);

app.get('/', async (req, res) => {
  const ret = await pool.query("select * from sensing order by time desc limit 15");
  res.send(ret[0]); 
})

io.on("connection", async(socket) => {
  const ret = await pool.query("select * from sensing order by time desc limit 15");
  socket.emit("kfc", ret[0]);

  socket.on("bbq", (arg) => {
    console.log(arg);
  })
})

server.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})