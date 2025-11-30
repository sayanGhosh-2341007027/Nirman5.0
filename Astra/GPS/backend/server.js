require('dotenv').config();
const express = require("express");
const http = require("http");
const mongoose = require("mongoose");
const cors = require("cors");
const socketIo = require("socket.io");
const ambulanceRoutes = require("./routes/ambulance");
const routeRoutes = require("./routes/route");

const app = express();
app.use(cors());
app.use(express.json());

app.use("/ambulance", ambulanceRoutes);
app.use("/route", routeRoutes);

const server = http.createServer(app);
const io = socketIo(server, { cors: { origin: "*" } });

// Socket to broadcast live locations
io.on("connection", (socket) => {
    console.log("Client connected.");

    socket.on("ambulance-location", (data) => {
        io.emit("location-update", data);  // send to all connected clients
    });

    socket.on("disconnect", () => {
        console.log("Client disconnected.");
    });
});

mongoose.connect("mongodb://localhost/ambulanceDB")
       .then(() => console.log("MongoDB connected"));

server.listen(5000, () => console.log("Server running on port 5000"));
