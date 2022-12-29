import businessrules as rules
import joblib
import logging


class ModelPred(rules.BusinessRules):
    def __init__(self):
        self._model = joblib.load("../data/finalized_model.sav")

    def prepare_dataset(self, X):
        logging.info("preparing the dataset...")
        # prepare dataset
        X = X
        return X

    def apply_business_rules(self, X):
        # business-rules.py  is used to define business rules
        return super().apply_business_rules(X)

    def apply_model_prediction(self, X):
        logging.info("second we will apply the ml-model for the hard-cases...")
        prediction_type = 'model_voorspelling'
        output = self._model.predict(X)
        return {'prediction_type': prediction_type,
                'prediction': output}

    def predict(self, X):
        X_prep = self.prepare_dataset(X)
        output_bl = self.apply_business_rules(X_prep)
        if output_bl:
            return f"We predict (bl) the following score for this neighborhood: {output_bl}"
        else:
            output_ml = self.apply_model_prediction(X_prep)
            return f"We predict (ml) the following score for this neighborhood: {output_ml}"