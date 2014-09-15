require 'json'
require 'csv'

jfile = File.open(ARGV[0], 'r')

if ARGV[1].nil?
  cfilename = File.basename(ARGV[0], 'json') + 'csv'
else
  cfilename = ARGV[1]
end

data = JSON.load(jfile)

CSV.open(cfilename, 'wb') do |csv|
  csv << data.first.map(&:first)

  data.each do |d|
    csv << d.map(&:last)
  end
end
