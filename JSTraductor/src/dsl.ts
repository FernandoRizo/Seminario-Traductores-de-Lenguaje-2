export type Primitive =
  | "string" | "integer" | "number" | "boolean"
  | "email" | "uuid" | "date" | "datetime" | "url";

export type NodeType = Primitive | "object" | "array";

export type Property = {
  type?: NodeType;
  enum?: (string | number | boolean | null)[];
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  minimum?: number;
  maximum?: number;
  pattern?: string;
  items?: Property;
  uniqueItems?: boolean;
  minItems?: number;
  maxItems?: number;
  description?: string;
  $ref?: string;               // referencia a otro modelo del DSL
};

export type Model = {
  type: "object";
  description?: string;
  additionalProperties?: boolean;
  properties?: Record<string, Property>;
  dependencies?: Record<string, string>; // "cond -> consequence"
};

export type DSL = {
  meta?: { id?: string; title?: string; version?: string };
  models: Record<string, Model>;
};

export type JSONSchema = Record<string, any>;
