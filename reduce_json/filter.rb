require 'json'

fin = File.open(ARGV[0], 'r')
fout = File.open(File.join(ARGV[1], File.basename(fin)), 'w')

keep = ARGV.slice(2,ARGV.size)

puts 'reading data'
data = JSON.load(fin)
fin.close()

smaller = []

data.each_with_index do |d, i|
  if i % 1000 == 0
    puts "#{i}/#{data.size}"
  end

  small = {}

  keep.each do |k|
    small[k] = d[k]
  end

  smaller << small
end

puts 'writing to ' + File.path(fout)
JSON.dump(smaller, fout)
fout.close()
