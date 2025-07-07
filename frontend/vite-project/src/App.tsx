import { useState, useEffect } from "react";
import Papa from "papaparse";
import "./App.css";

// Define a type for our player data for type safety
interface Player {
  Player: string;
  Projected_Pts: number;
  VBD: number;
}

function App() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const csvFilePath = "/2025_projections.csv";

    Papa.parse<Player>(csvFilePath, {
      download: true,
      header: true,
      dynamicTyping: true,
      complete: (results) => {
        // Filter out any rows that might be empty or don't have a player name
        const validPlayers = results.data.filter(
          (p) => p.Player && p.VBD !== null
        );
        setPlayers(validPlayers);
      },
      error: (err) => {
        setError("Failed to load or parse the CSV file.");
        console.error("PapaParse Error:", err);
      },
    });
  }, []); // Empty dependency array ensures this runs only once

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="App">
      <h1>Fantasy Football Projections 2025</h1>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Player</th>
            <th>Projected Pts</th>
            <th>VBD</th>
          </tr>
        </thead>
        <tbody>
          {players.map((player, index) => (
            <tr key={player.Player || index}>
              <td>{index + 1}</td>
              <td>{player.Player}</td>
              <td>{player.Projected_Pts?.toFixed(2)}</td>
              <td>{player.VBD?.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
