import businessrules as rules
import joblib
import logging


class BuurtenModel(rules.BusinessRulesOne, rules.BusinessRulesTwo):
    def __init__(self):
        self._model_one = joblib.load("../data/finalized_model.sav")
        self._model_two = joblib.load("../data/finalized_model.sav")

    def prepare_dataset(self, X):
        logging.info("preparing the dataset...")
        # prepare dataset
        X = X
        return X

    def apply_business_rules_one(self, X):
        # business-rules.py  is used to define business rules
        return super().apply_business_rules_one(X)

    def apply_business_rules_two(self, X):
        # business-rules.py  is used to define business rules
        return super().apply_business_rules_two(X)

    def apply_model_prediction_one(self, X):
        logging.info("second we will apply the ml-model for the hard-cases...")
        prediction_type = 'model_voorspelling'
        output = self._model_one.predict(X)
        return {'prediction_type_one': prediction_type,
                'prediction_one': output}

    def apply_model_prediction_two(self, X, ):
        logging.info("second we will apply the ml-model for the hard-cases...")
        prediction_type = 'model_voorspelling'
        output = self._model_two.predict(X)
        return {'prediction_type_two': prediction_type,
                'prediction_two': output}            

    def predict(self, X):

        # prepare dataset
        X_prep = self.prepare_dataset(X)

        # apply first business rules (returns json or empty)
        output_bl = self.apply_business_rules_one(X_prep)

        # if output_bl filled, return as output, otherwise prediction with model
        output_step_one = [output_bl if output_bl else self.apply_model_prediction_one(X_prep)]

        # based on first predictionn, apply business rules part two
        output_bl_two = self.apply_business_rules_two(X_prep, output_step_one)

        # if output_final
        if output_bl_two['prediction_type_two'] == "model_voorspelling":
            output_bl_two['prediction_two'] = self.apply_model_prediction_two(X_prep)

        return output_bl_two
