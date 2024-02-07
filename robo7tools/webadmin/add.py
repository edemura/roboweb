from models import ConfigType

p = ConfigType(configtype="New")
p.save()
print(p.configtype)