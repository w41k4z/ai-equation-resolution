import express from "express";
import cors from "cors";
import multer from "multer";
import { execSync } from "child_process";

const server = express();
const upload = multer({ dest: "src/uploads" });

server.use(cors());
server.use(express.json());

server.post(
  "/ai-model/expression-detection",
  upload.single("image"),
  (req, res) => {
    if (req.file) {
      try {
        const command = `python3 src/MLModel/ml_equation_model.py '${req.file.path}'`;
        const output = execSync(command).toString().trim();
        res.status(200).json({ result: output });
      } catch (error) {
        res.status(500).json({ message: error });
        console.log(error);
      }
    } else {
      console.log("No file uploaded");
    }
  }
);

server.post("/ai-model/expression-eval", (req, res) => {
  try {
    const command = `python3 src/MLModel/equation_resolver.py '${req.body.expression}'`;
    const output = execSync(command).toString().trim();
    res.status(200).json({ result: output });
  } catch (error) {
    res.status(500).json({ message: error });
    console.log(error);
  }
});

server.listen(5000, () => {
  console.log("Server is running on port 5000");
});
