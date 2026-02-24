from datetime import datetime, timedelta

class SampleCaching:
      head = 0
      def __init__(self,default_ttl = 30):
            self.head += 1
            self.cache = {}
            self.default_ttl = default_ttl
      
      def get(self,key):
            if key in self.cache.keys():
                  data , exp = self.cache[key]
                  if datetime.now() < exp:
                        return data
                  else:
                        self.delete(key)

      def set(self,key , value):
            expiry = datetime.now() + timedelta(seconds=self.default_ttl)
            self.cache[key] = (value, expiry)


      def delete(self,key):
            del self.cache[key]

      def get_stats(self):
            return {
            "total_keys": len(self.cache),
            "keys": list(self.cache.keys()),
            "default_ttl": self.default_ttl
      }