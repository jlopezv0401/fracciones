require 'rubygems'
require 'nokogiri'
require 'mysql'

db = Mysql::new('192.168.40.240', 'root', 'moises', 'fracciones')

results = db.query "SELECT txt FROM fracciones"
x=0

results.each do |row|
  if (x<1)
    #print row[0]
    
    doc = Nokogiri::HTML(row)
    print doc.at_css('body').text
    x+=1
  end
end

