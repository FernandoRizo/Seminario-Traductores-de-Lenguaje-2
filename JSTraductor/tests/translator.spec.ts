import { describe, it, expect } from "vitest";
import { parseDSL } from "../src/parser.js";
import { dslToJSONSchema } from "../src/jsonschema.js";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

describe("Translator", () => {
  it("convierte DSL a JSON Schema y agrega reglas", () => {
    const dsl = parseDSL(resolve("tests/fixtures/schema.yml"));
    const schema = dslToJSONSchema(dsl);
    expect(schema.$schema).toBeDefined();
    expect(schema.definitions?.User).toBeDefined();
    const user = schema.definitions!.User;
    expect(user.properties.email).toBeDefined();
    // Required básicos
    expect(new Set(user.required)).toContain("name");
    // Regla if/then generada
    expect(user.allOf?.length || 0).toBeGreaterThan(0);
  });
});
