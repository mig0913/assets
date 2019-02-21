def dict_merge(dct, merge_dct):
    for k, v in merge_dct.iteritems():
        if (k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]
    return dct



dict1 = { 'IP' : '127.0.0.1','Desktop' : ' ' , 'Server' : 'True', 'SSL' : 'True'}
dict2 = { 'IP' : '127.0.0.1', 'Desktop' : 'True ' , 'Server' : 'True', 'SSL' : ''}


   irint d
