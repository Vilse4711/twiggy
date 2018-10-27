class Production:
    
    def produce(self,actuals,data):
        raise LException("Abstract method: LProduction.produce()")

    def context(self):
        raise LException("Abstract method: LProduction.formals()")
