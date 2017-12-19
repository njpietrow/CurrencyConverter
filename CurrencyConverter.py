from lxml import html
import requests
import BeautifulSoup

session = requests.session()

page = requests.get('http://x-rates.com/table/?from=USD&amount=1')
tree = html.fromstring(page.content)

currencies = tree.xpath('//*[@id="content"]/div[1]/div/div[1]/div[1]/table[2]/tbody/tr[position() > 0 and not(position > 53)]/td[1]/text()')
fromdollar = tree.xpath('//*[@id="content"]/div[1]/div/div[1]/div[1]/table[2]/tbody/tr[position() > 0 and not(position > 53)]/td[2]/a/text()')
invdollar = tree.xpath('//*[@id="content"]/div[1]/div/div[1]/div[1]/table[2]/tbody/tr[position() > 0 and not(position > 53)]/td[3]/a/text()')
time = tree.xpath('//*[@id="content"]/div[1]/div/div[1]/div[1]/span[4]/text()')
timeelem = time[0]
frommap = {} #map from currency to USD convrate
invmap = {} #map from curr to USD invrate

count = 0
for i in currencies:
	frommap[i] = fromdollar[count]
	invmap[i] = invdollar[count]
	count += 1
currencies.append('US Dollar')
frommap['US Dollar'] = 1.0
invmap['US Dollar'] = 1.0

print "=================CURRENCIES as of %s ================="%timeelem
for a,b,c in zip(currencies[::3],currencies[1::3],currencies[2::3]):
	print '{:<30}{:<30}{:<}'.format(a,b,c)
while 1:
	incurrency = raw_input('Enter currency to convert from or q to quit >> ')
	if incurrency  == 'q':
		exit(0)
	try:
		todollar = invmap[incurrency]
	except KeyError:
		print "\tNot a Valid Currency"
		continue
	else:
		break
while 1:
	# print "=================CURRENCIES as of %s ================="%timeelem
	# for a,b,c in zip(currencies[::3],currencies[1::3],currencies[2::3]):
	# 	print '{:<30}{:<30}{:<}'.format(a,b,c)
	outcurrency = raw_input('Enter currency to convert to or q to quit >> ')
	if outcurrency  == 'q':
		exit(0)
	try:
		fromdollar = frommap[outcurrency]
	except KeyError:
		print "\tNot a Valid Currency"
		continue
	else:
		break
while 1:
	val = raw_input('Enter value to convert >> ')
	try:
   		convnum = float(val)
	except ValueError:
   		print("\tPlease enter a valid value")
   		continue
   	else:
   		break

if incurrency ==outcurrency:
	print "%f %s is equal to \n%f %s" %(convnum,incurrency,convnum,outcurrency)
else:
	returnval =  convnum * float(todollar) * float(fromdollar)
	print "%f %s is equal to \n%f %s" %(convnum,incurrency,returnval,outcurrency)





