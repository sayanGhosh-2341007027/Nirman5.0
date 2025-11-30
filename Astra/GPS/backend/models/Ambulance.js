const mongoose = require("mongoose");

const ambulanceSchema = new mongoose.Schema({
    name: String,
    latitude: Number,
    longitude: Number,
    isActive: { type: Boolean, default: false }
});

module.exports = mongoose.model("Ambulance", ambulanceSchema);
