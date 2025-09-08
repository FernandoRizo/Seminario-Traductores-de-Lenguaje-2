import { validateAll } from "./dist/generated/validators/ajv.js";


const okData = {
  User: {
    id: "9d8a2d8a-0f7d-4813-9a06-3d5b7a2d1111",
    name: "Ana",
    email: "ana@example.com",
    roles: ["admin"]
  },
  Profile: { website: "https://mi.site" }
};

console.log("OK?", validateAll(okData), validateAll.errors);

const badData = { User: { id: "bad", name: "A", roles: [] }, Profile: {} };
console.log("OK?", validateAll(badData), validateAll.errors);
