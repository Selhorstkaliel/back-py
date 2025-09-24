require_relative "config"
require 'tzinfo/data' if Gem.win_platform?
require "rufus-scheduler"

scheduler = Rufus::Scheduler.new

# Job diário para atualizar status das entries
scheduler.cron "0 3 * * *" do # 3h da manhã todo dia
  now = Time.now

  DB[:entries].where(status: STATUS[:restricao]).where{created_at < now - 30*24*60*60}.update(status: STATUS[:finalizado])
  DB[:entries].where{created_at < now - 180*24*60*60}.update(status: STATUS[:reprotocolo])

  puts "[#{Time.now}] Entries atualizadas pelo scheduler."
end

# Cria restrição em novos cadastros (opcional, já nasce assim)
# DB[:entries].where(status: nil).update(status: STATUS[:restricao])

puts "Scheduler iniciado. Pressione Ctrl+C para sair."
scheduler.join