function toJSONSchemaType(prop) {
    if (prop.$ref) {
        return { $ref: `#/definitions/${prop.$ref}` };
    }
    if (prop.enum)
        return { enum: prop.enum };
    switch (prop.type) {
        case "string": return { type: "string" };
        case "integer": return { type: "integer" };
        case "number": return { type: "number" };
        case "boolean": return { type: "boolean" };
        case "email": return { type: "string", format: "email" };
        case "uuid": return { type: "string", format: "uuid" };
        case "date": return { type: "string", format: "date" };
        case "datetime": return { type: "string", format: "date-time" };
        case "url": return { type: "string", format: "uri" };
        case "array": {
            if (!prop.items)
                throw new Error("Array sin 'items'");
            return {
                type: "array",
                items: toJSONSchemaProp(prop.items),
                ...(prop.uniqueItems !== undefined ? { uniqueItems: prop.uniqueItems } : {}),
                ...(prop.minItems !== undefined ? { minItems: prop.minItems } : {}),
                ...(prop.maxItems !== undefined ? { maxItems: prop.maxItems } : {}),
            };
        }
        default:
            return {}; // se completa en toJSONSchemaProp
    }
}
function toJSONSchemaProp(prop) {
    const base = toJSONSchemaType(prop);
    if (prop.description)
        base.description = prop.description;
    if (prop.minLength !== undefined)
        base.minLength = prop.minLength;
    if (prop.maxLength !== undefined)
        base.maxLength = prop.maxLength;
    if (prop.minimum !== undefined)
        base.minimum = prop.minimum;
    if (prop.maximum !== undefined)
        base.maximum = prop.maximum;
    if (prop.pattern)
        base.pattern = prop.pattern;
    return base;
}
function modelToSchema(name, m) {
    const properties = {};
    const required = [];
    for (const [key, p] of Object.entries(m.properties || {})) {
        properties[key] = toJSONSchemaProp(p);
        if (p.required)
            required.push(key);
    }
    const schema = {
        type: "object",
        ...(m.description ? { description: m.description } : {}),
        properties,
        ...(m.additionalProperties === false ? { additionalProperties: false } : {}),
        ...(required.length ? { required } : {})
    };
    // dependencies: soporta "roles includes 'admin' -> email required"
    if (m.dependencies) {
        const allOf = [];
        for (const [_k, rule] of Object.entries(m.dependencies)) {
            const match = rule.match(/^(.+)\s*->\s*(.+)$/);
            if (!match)
                continue;
            const [_, cond, cons] = match;
            // cond: "roles includes 'admin'"
            const condMatch = cond.match(/^(\w+)\s+includes\s+'(.+)'$/);
            // cons: "email required"
            const consMatch = cons.match(/^(\w+)\s+required$/);
            if (condMatch && consMatch) {
                const field = condMatch[1], value = condMatch[2];
                const reqField = consMatch[1];
                allOf.push({
                    if: {
                        properties: {
                            [field]: {
                                anyOf: [
                                    { const: value },
                                    { type: "array", contains: { const: value } }
                                ]
                            }
                        }
                    },
                    then: { required: [reqField] }
                });
            }
        }
        if (allOf.length)
            schema.allOf = allOf;
    }
    return schema;
}
export function dslToJSONSchema(dsl) {
    const definitions = {};
    for (const [name, model] of Object.entries(dsl.models)) {
        definitions[name] = modelToSchema(name, model);
    }
    return {
        $schema: "https://json-schema.org/draft/2020-12/schema",
        $id: dsl.meta?.id || "generated.schema",
        title: dsl.meta?.title,
        type: "object",
        properties: Object.fromEntries(Object.keys(dsl.models).map(k => [k, { $ref: `#/definitions/${k}` }])),
        additionalProperties: false,
        definitions
    };
}
