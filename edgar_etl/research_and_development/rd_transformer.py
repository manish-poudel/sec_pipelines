class RDTransformer:

    @staticmethod
    def compute_zscore(df):
        df = df.groupby(['fiscal_year', 'fiscal_period', 'cik'], as_index=False).agg({
            "filed": "first",
            "rd_expense": "sum"
        })

        grouped_df = df.groupby(['fiscal_year', 'fiscal_period'])
        df['rd_expense_mean'] = grouped_df['rd_expense'].transform('mean')
        df['rd_expense_std'] = grouped_df['rd_expense'].transform('std')

        # Compute the Z-score
        df['z_score'] = (df['rd_expense'] - df['rd_expense_mean']) / df['rd_expense_std']
        df = df.drop(columns=['rd_expense_mean', 'rd_expense_std'])

        return df










