const express = require("express");
const axios = require("axios");
const Hospital = require("../models/Hospital");
const Ambulance = require("../models/Ambulance");
const router = express.Router();

// replace any hard-coded key with the env var
const GOOGLE_API_KEY = process.env.GOOGLE_MAPS_API_KEY || "";

router.get("/fastest/:id", async (req, res) => {
    const amb = await Ambulance.findById(req.params.id);
    if (!amb) return res.status(404).json({ msg: "Ambulance not found" });

    const hospitals = await Hospital.find();
    let nearest = hospitals[0];

    // Simple straight-line nearest hospital
    hospitals.forEach((h) => {
        const dist = Math.hypot(
            h.latitude - amb.latitude, 
            h.longitude - amb.longitude
        );
        if (dist < Math.hypot(nearest.latitude - amb.latitude, nearest.longitude - amb.longitude)) {
            nearest = h;
        }
    });

    // Google Maps API
    const url = `https://maps.googleapis.com/maps/api/directions/json?origin=${amb.latitude},${amb.longitude}&destination=${nearest.latitude},${nearest.longitude}&key=${GOOGLE_API_KEY}`;

    const response = await axios.get(url);

    res.json({
        ambulance: amb.name,
        hospital: nearest.name,
        route: response.data.routes[0]
    });
});

// New endpoint: accepts ?start=lng,lat&end=lng,lat and returns GeoJSON-like features[0].geometry.coordinates
router.get("/fastest-route", async (req, res) => {
    try {
        const { start, end } = req.query;
        if (!start || !end) return res.status(400).json({ msg: "start and end query params required" });

        const [startLon, startLat] = start.split(",").map(Number);
        const [endLon, endLat] = end.split(",").map(Number);

        // Use public OSRM server to get geojson coordinates (lng,lat)
        const osrmUrl = `http://router.project-osrm.org/route/v1/driving/${startLon},${startLat};${endLon},${endLat}?overview=full&geometries=geojson`;
        const resp = await axios.get(osrmUrl);

        if (!resp.data || !resp.data.routes || resp.data.routes.length === 0) {
            return res.status(500).json({ msg: "No route from routing engine" });
        }

        const coordinates = resp.data.routes[0].geometry.coordinates; // [[lng,lat], ...]

        // Return a structure matching what frontend expects: res.data.features[0].geometry.coordinates
        return res.json({
            features: [
                {
                    geometry: {
                        coordinates
                    }
                }
            ]
        });
    } catch (err) {
        console.error("fastest-route error:", err.message || err);
        return res.status(500).json({ msg: "Failed to fetch route", error: err.message });
    }
});

module.exports = router;
