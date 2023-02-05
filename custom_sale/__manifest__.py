{
    'name':'Custom Sale Extend',
    'website':'https://google.com',
    'summery':'This is Custom Extended Sale Summery',
    'version':'1.0',
    'description':
        """
abcd

This is Custom Extended Sale Descsription.
------------------------------------------

    *a
    *b
    *c
    *d
        """,
    'depends':['base','custom'],
    'data':['views/custom_sale_extend.xml',
            'security/ir.model.access.csv'],
    'demo':[],
    'installable':True,
}