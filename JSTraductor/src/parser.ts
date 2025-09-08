import { load } from "js-yaml";
// ⬇⬇⬇ sin 'node:' ⬇⬇⬇
import { readFileSync } from "fs";
import { DSL, Model } from "./dsl.js";

export function parseDSL(path: string): DSL {
  const raw = readFileSync(path, "utf8");
  const doc = load(raw) as any;

  if (!doc || typeof doc !== "object") throw new Error("DSL inválido");
  if (!doc.models || typeof doc.models !== "object")
    throw new Error("DSL inválido: falta 'models'");

  for (const [name, m] of Object.entries<Model>(doc.models)) {
    if (m.type !== "object") {
      throw new Error(`El modelo '${name}' debe ser type: object`);
    }
  }
  return doc as DSL;
}
