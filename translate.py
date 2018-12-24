import googletrans

class Trans():
    def __init__(self):
        self.translator = googletrans.Translator()
        self.outputlang = 'ko_KR'
    
    def setlang(self, lang: str):
        self.outputlang = lang

    def get(self):
        return self.outputlang

    def gettext(self, text: str):
        if self.outputlang == 'ko_KR' or 'en_US':
            return text
        return self.translator.translate(text, dest=self.outputlang).text
    
    def temprun(self, text: str, src:str, dest:str):
        return self.translator.translate(text, src=src, dest=dest).text   

trans = Trans()
