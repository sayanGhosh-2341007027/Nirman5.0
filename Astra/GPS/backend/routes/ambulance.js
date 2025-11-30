const express = require("express");
const router = express.Router();
const Ambulance = require("../models/Ambulance");

router.post("/update", async (req, res) => {
    const { id, latitude, longitude } = req.body;

    let amb = await Ambulance.findById(id);
    if (!amb) return res.status(404).json({ msg: "Ambulance not found" });

    amb.latitude = latitude;
    amb.longitude = longitude;
    amb.isActive = true;
    await amb.save();

    res.json({ msg: "Location updated" });
});

module.exports = router;
