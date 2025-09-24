require "dotenv/load"
require "sequel"

DB_PATH = ENV["SQLITE_PATH"] || "../server/data/dev.sqlite"
DB = Sequel.sqlite(DB_PATH)

# Conveniência: enums dos status
STATUS = {
  restricao: "Restrição",
  finalizado: "Finalizado",
  reprotocolo: "Reprotocolo"
}