import logging

class BusinessRules:
    """
    Define business rules to apply to dataframe.

    Attributes:
        X (pd.DataFrame): features that are needed to
        determine if business rules apply to this item.

    """
    def __init__(self):
        pass

    def apply_business_rules(self, X):       
        logging.info('first we will apply the business-rules for all the cases (where possible)...')

        # business-rule 1: check if feature one is bigger than
        if X[0][0] > 350:
            logging.info('based on business rule 1')
            return 2000

        # business-rule 2: check if feature two is bigger than
        elif X[0][1] > 12:
            logging.info('based on business rule 2')
            return 2000

        # when no business-rule is applicable, we pass it to the ML-model
        else:
            logging.info('no business-rule applicable..')
            pass
