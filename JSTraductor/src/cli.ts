#!/usr/bin/env node
import { Command } from "commander";
import { parseDSL } from "./parser.js";
import { dslToJSONSchema } from "./jsonschema.js";
import { generateAjvModule } from "./generators/ajv.js";
import { generateZodModule } from "./generators/zod.js";
import { generateJoiModule } from "./generators/joi.js";
import { writeFileRecursive } from "./util.js";
import { resolve, join } from "node:path";
import { fileURLToPath } from "node:url";
import { readFileSync, mkdirSync, writeFileSync } from "node:fs";

const program = new Command();

program
  .name("schema-gen")
  .description("Traduce un DSL YAML a JSON Schema y genera validadores (Ajv/Zod/Joi).")
  .option("-i, --in <path>", "Ruta al schema YAML", "schema.yml")
  .option("-t, --target <name>", "ajv | zod | joi | all", "all")
  .option("-o, --out <dir>", "directorio de salida", "dist")
  .option("--emit-json", "Emitir el JSON Schema raíz", false)
  .action(async (opts) => {
    const dsl = parseDSL(resolve(opts.in));
    const jschema = dslToJSONSchema(dsl);

  
    if (opts.emitJson) {
      const p = join(opts.out, "schema.json");
      mkdirSync(opts.out, { recursive: true });
      writeFileSync(p, JSON.stringify(jschema, null, 2), "utf8");
      console.log("Esquema JSON guardado en:", p);
    }

    const want = (k: string) => opts.target === "all" || opts.target === k;

    if (want("ajv")) {
      const mod = generateAjvModule(jschema, "validateAll");
      writeFileRecursive(join(opts.out, "validators", "ajv.ts"), mod);
    }
    if (want("zod")) {
      const mod = generateZodModule(jschema);
      writeFileRecursive(join(opts.out, "validators", "zod.ts"), mod);
    }
    if (want("joi")) {
      const mod = generateJoiModule(jschema);
      writeFileRecursive(join(opts.out, "validators", "joi.ts"), mod);
    }

    console.log("Generación completa en", resolve(opts.out));
  });

program.parse();
