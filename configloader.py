import ConfigParser

config = ConfigParser.SafeConfigParser()
config.read('options.conf')
print(config.sections())
#config.get('section','option',0)
print(config.get('email','password',1))
print('done')
