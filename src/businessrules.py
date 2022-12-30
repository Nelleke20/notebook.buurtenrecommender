import logging


class BusinessRulesOne:
    """
    Define business rules to apply to dataframe.

    Attributes:
        X (pd.DataFrame): features that are needed to
        determine if business rules apply to this item.

    """

    def __init__(self):
        pass

    def apply_business_rules_one(self, X):
        logging.info(" apply the like business-rules for all (possible) cases")

        # business-rule 1: check if feature one is bigger than
        if X[0][0] > 350:
            prediction_type_one = "business rule 1a"
            logging.info("based on business rule 1a")
            return {"prediction_type_one": prediction_type_one, "prediction_one": 20}

        # business-rule 2: check if feature two is bigger than
        elif X[0][1] > 12:
            prediction_type_one = "business rule 1b"
            logging.info("based on business rule 1b")
            return {"prediction_type_one": prediction_type_one, "prediction_one": 10}

        # when no business-rule is applicable, we pass it to the ML-model
        else:
            prediction_type_one = "model_voorspelling"
            logging.info("no business-rule applicable..")
            return {"prediction_type_one": prediction_type_one}


class BusinessRulesTwo:
    """
    Define business rules to apply to dataframe.

    Attributes:
        X (pd.DataFrame): features that are needed to
        determine if business rules apply to this item.

    """

    def __init__(self):
        pass

    def apply_business_rules_two(self, X, output):
        logging.info("Apply the business-rules for all (possible) cases")

        prediction_type_one = output["prediction_type_one"]
        prediction_one = output["prediction_one"][0]

        # business-rule 2a: check if feature one is bigger than
        if (X[0][0] == 400) & (prediction_one == 20):
            output['prediction_type_two'] = "business rule 2a"
            output['prediction_two'] = 1992
            logging.info("based on business rule 2a")

        # business-rule 2b: check if feature two is bigger than
        elif (X[0][1] == 850) & (prediction_one == 10):
            output['prediction_type_two'] = "business rule 2b"
            output['prediction_two'] = 0.10
            logging.info("based on business rule 2b")

        # when no business-rule is applicable, we pass it to the ML-model
        else:
            logging.info("no business-rule applicable..")
            output['prediction_type_two'] = "model_voorspelling"
            output['prediction_two'] = "model_voorspelling"

        return {
                "prediction_type_one": prediction_type_one,
                "prediction_one": prediction_one,
                "prediction_type_two": output['prediction_type_two'],
                "prediction_two": output['prediction_two']
            }