#! /usr/bin/python3 -u

def parseConfigFile(file):
    f=open(file,'r')
    try:
        formatted_content=""
        for line in f:
            if "#" not in line:
                line=line.strip().replace(' ','').replace('\n','').replace('\t','')
                if line!="":
                    formatted_content+=line

        resources={}
        for group in formatted_content.split('};'):
            group=group.split('{')
            if group!=[""]:
                name=group[0]
                c_group=group[1]

                c_group_res={}
                resources[name]=c_group_res
                for k_v in c_group.split(';'):
                    k_v=k_v.split(':')
                    if k_v!=[""]:
                        k=k_v[0]
                        v=float(k_v[1])
                        if name=='patterns':
                            c_group_res[k]=v
                        else:
                            for ch in k:
                                c_group_res[ch]=v

    finally:
        f.close()

    return resources

def processPercentages(group):
    keys=list(group.keys())
    values=list(group.values())
    s=""
    for i in range(len(keys)):
        s+=keys[i].lower()*int(values[i]*int(100))

    # Mixure
    import random
    s=list(s)
    l=len(s)
    for i in range(l):
        j=i%l
        k=random.randint(0, l-1)
        a=s[j]
        b=s[k]
        s[j]=b
        s[k]=a

    return s

def translatePattern(pattern, vowels, consonants):
    import random
    for i in range(len(pattern)):
        if pattern[i]=='V':
            pattern[i]=random.choice(vowels)
        else:
            pattern[i]=random.choice(consonants)
    return pattern



def pwGenerator(resources, min, max):
    vowels=processPercentages(resources["vowels"])
    consonants=processPercentages(resources["consonants"])
    patterns=resources["patterns"]

    patt_k=list(patterns.keys())
    patt_v=list(patterns.values())

    accum=patt_v.copy()
    for i in range(1,len(accum)):
        accum[i]=accum[i-1]+accum[i]
    max_accum=accum[-1]
    import random
    while True:
        l=random.randint(min,max)
        print("l="+str(l))
        pw=""
        while l>0:
            p=None
            n=random.randint(0,int(max_accum*100))/100.0
            for i in range(len(accum)):
                if accum[i]>=n:
                    # Pattern patt_k[i]
                    p = patt_k[i]
                    break
            if len(pw)+len(p)>l:
                pw+=random.choice(['V','C'])
                l-=1
            else:
                pw+=p
                l-=len(p)
        yield "".join(translatePattern(list(pw),vowels,consonants))



def main(file, min, max):
    print("[*] Parsing "+str(file)+"...")
    resources=parseConfigFile(file)
    try:
        pw=pwGenerator(resources, min, max)
        while True:
            print(pw.__next__())
    except KeyboardInterrupt:
        print("\n[*] Stopped by user!")


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser("RAGEN-WL: Random Generator for WordLists.")
    parser.add_argument('-f', dest='file', required=True, help="Configuration file")
    parser.add_argument('--min', '-m',  dest='min_l', default=8, type=int, help="Minimum length of the password (included) [Default=8]")
    parser.add_argument('--max', '-M',  dest='max_l', default=20, type=int, help="Maximum length of the password (included) [Default=20]")
    args=parser.parse_args()

    if args.min_l>args.max_l:
        parser.error("Minimum length cannot be greater than maximum length")

    import os.path
    if not os.path.isfile(args.file):
        parser.error("'"+args.file+"' does not exist")


    main(args.file, args.min_l, args.max_l)
