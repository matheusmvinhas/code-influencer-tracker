CREATE SCHEMA IF NOT EXISTS influencer;

CREATE TABLE influencer.brands (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "cnpj" varchar,
  "contact_email" varchar,
  "website" varchar,
  "instagram_handle" varchar,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE influencer.creators (
  "id" integer PRIMARY KEY,
  "cpf" varchar,
  "username" varchar,
  "email" varchar,
  "instagram_handle" varchar,
  "role" varchar,
  "bio" text,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE influencer.brand_creator_links (
  "id" integer PRIMARY KEY,
  "creator_id" integer,
  "brand_id" integer,
  "partnership_type" varchar,
  "status" varchar,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE influencer.creator_codes (
  "id" integer PRIMARY KEY,
  "creator_id" integer,
  "brand_id" integer,
  "code" varchar UNIQUE,
  "discount" decimal,
  "commission" decimal,
  "is_percentage" boolean,
  "usage_limit" integer,
  "times_used" integer,
  "status" varchar,
  "started_at" timestamp,
  "disabled_at" timestamp,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE influencer.orders (
  "id" integer PRIMARY KEY,
  "external_order_id" varchar,
  "date" date,
  "brand_id" integer,
  "code" varchar,
  "order_price" decimal,
  "discount" decimal,
  "total_paid" decimal,
  "currency" varchar,
  "status" varchar,
  "customer_email" varchar,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE influencer.order_lines (
  "id" integer PRIMARY KEY,
  "order_id" integer,
  "product_id" varchar,
  "product_name" varchar,
  "sku" varchar,
  "quantity" integer,
  "unit_price" decimal,
  "created_at" timestamp
);

CREATE TABLE influencer.commissions (
  "id" integer PRIMARY KEY,
  "creator_id" integer,
  "order_id" integer,
  "code_id" integer,
  "commission_value" decimal,
  "status" varchar,
  "paid_at" timestamp,
  "created_at" timestamp
);

CREATE TABLE influencer.code_logs (
  "id" integer PRIMARY KEY,
  "code_id" integer,
  "event" varchar,
  "metadata" json,
  "created_at" timestamp
);

COMMENT ON COLUMN "brand_creator_links"."partnership_type" IS 'e.g., affiliate, ambassador';

COMMENT ON COLUMN "brand_creator_links"."status" IS 'active, inactive, pending';

COMMENT ON COLUMN "creator_codes"."commission" IS 'commission in % or fixed value';

COMMENT ON COLUMN "creator_codes"."usage_limit" IS 'null = unlimited';

COMMENT ON COLUMN "orders"."external_order_id" IS 'e.g., Shopify ID';

COMMENT ON COLUMN "orders"."code" IS 'Used discount code';

COMMENT ON COLUMN "orders"."status" IS 'paid, refunded, canceled';

COMMENT ON COLUMN "commissions"."status" IS 'pending, paid, reversed';

COMMENT ON COLUMN "code_logs"."event" IS 'used, disabled, created, updated';

ALTER TABLE influencer.brand_creator_links ADD FOREIGN KEY ("creator_id") REFERENCES influencer.creators ("id");

ALTER TABLE influencer.brand_creator_links ADD FOREIGN KEY ("brand_id") REFERENCES influencer.brands ("id");

ALTER TABLE influencer.creator_codes ADD FOREIGN KEY ("creator_id") REFERENCES influencer.creators ("id");

ALTER TABLE influencer.creator_codes ADD FOREIGN KEY ("brand_id") REFERENCES influencer.brands ("id");

ALTER TABLE influencer.orders ADD FOREIGN KEY ("brand_id") REFERENCES influencer.brands ("id");

ALTER TABLE influencer.order_lines ADD FOREIGN KEY ("order_id") REFERENCES influencer.orders ("id");

ALTER TABLE influencer.commissions ADD FOREIGN KEY ("creator_id") REFERENCES influencer.creators ("id");

ALTER TABLE influencer.commissions ADD FOREIGN KEY ("order_id") REFERENCES influencer.orders ("id");

ALTER TABLE influencer.commissions ADD FOREIGN KEY ("code_id") REFERENCES influencer.creator_codes ("id");

ALTER TABLE influencer.code_logs ADD FOREIGN KEY ("code_id") REFERENCES influencer.creator_codes ("id");


-- 1. Garante que a coluna times_used existe
-- ALTER TABLE creator_codes
-- ADD COLUMN IF NOT EXISTS times_used integer DEFAULT 0;

-- -- 2. Cria a função que incrementa o contador
-- CREATE OR REPLACE FUNCTION increment_code_usage()
-- RETURNS TRIGGER AS $$
-- BEGIN
--   -- Atualiza o campo times_used quando o pedido for válido
--   UPDATE creator_codes
--   SET times_used = times_used + 1
--   WHERE code = NEW.code
--     AND brand_id = NEW.brand_id;  -- garante match com a marca também

--   RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- -- 3. Cria o trigger que executa após um INSERT em orders
-- CREATE TRIGGER trg_increment_code_usage
-- AFTER INSERT ON orders
-- FOR EACH ROW
-- WHEN (
--   NEW.code IS NOT NULL
--   AND NEW.status = 'paid'
-- )
-- EXECUTE FUNCTION increment_code_usage();