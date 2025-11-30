import { MapContainer, TileLayer, Polyline, Marker, Popup } from "react-leaflet";
import { useState } from "react";
import axios from "axios";
import "leaflet/dist/leaflet.css";

export default function RouteMap() {
  const [routeCoords, setRouteCoords] = useState([]);
  const [start] = useState([28.6139, 77.2090]); // Delhi (lat, lng)
  const [end] = useState([28.6500, 77.3000]);   // Hospital example

  // Convert [lng, lat] to [lat, lng]
  const convertCoords = (coords) => coords.map(c => [c[1], c[0]]);

  const getRoute = async () => {
    try {
      const res = await axios.get("http://localhost:5000/route/fastest-route", {
        params: {
          start: `${start[1]},${start[0]}`, // lng,lat
          end: `${end[1]},${end[0]}`        // lng,lat
        }
      });

      const geometry = res.data.features[0].geometry.coordinates;
      const converted = convertCoords(geometry);
      setRouteCoords(converted);

    } catch (err) {
      console.error("Failed to fetch route", err);
    }
  };

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <button 
        onClick={getRoute} 
        style={{
          position: "absolute",
          zIndex: 9999,
          padding: "10px",
          background: "#007bff",
          color: "#fff",
          borderRadius: "6px",
          border: "none",
          cursor: "pointer",
          margin: "10px"
        }}
      >
        Get Fastest Route
      </button>

      <MapContainer
        center={start}
        zoom={13}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {/* Start Marker */}
        <Marker position={start}>
          <Popup>Ambulance Start Point</Popup>
        </Marker>

        {/* End Marker */}
        <Marker position={end}>
          <Popup>Hospital</Popup>
        </Marker>

        {/* Draw Route */}
        {routeCoords.length > 0 && (
          <Polyline positions={routeCoords} color="blue" />
        )}
      </MapContainer>
    </div>
  );
}
