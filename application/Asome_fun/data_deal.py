# ###处理数据得到csv表格文件
import csv
import time
import os
import re


# ##保存日志写入文件
def save_log(data, log_file_name='insects_log', path='E:/A`毕业设计/蜜蜂数据处理/蜜蜂test/'):
    '''
    data处理:save data处理;
    log_file_name default is 'insects_log';
    path default is 'E:\A`毕业设计\蜜蜂数据处理\蜜蜂test;
    '''
    if not os.path.isdir(path):
        os.makedirs(path)
    out_log = open(path + log_file_name + '.txt', 'a+')
    out_log.write('\n')
    if type(data) is str:
        out_log.write(data)
    if type(data) is list:
        for line in data:
            out_log.write('\n' + line)
    out_log.close


# ###cds文件：———基因序列表（Gene_seq）：物种名，基因名，功能，序列
def cds(cds_file_path, table_path):
    fcds = open(cds_file_path, "r")  # 以读方式打开cds文件
    species = {}  # 物种字典
    gene = {}  # 基因字典
    func = {}  # 功能字典
    seq = {}  # 定义序列字典
    for line in fcds.readlines():
        if line.startswith('>'):
            space = line.index(" ")  # 找到空格位置
            part1 = line[1:space]  # 提取到part1即基因名称列
            left = line.index("(")  # 找到左括号位置，例如(LOC107992398)
            # 判断如果存在“PREDICTED:”，找到“：”位置，提取"："以后以及“（”以前的字符串
            if "PREDICTED:" in line:
                PREDICTED = line.index(":")
                spec_fun = line[PREDICTED + 2:left - 1]
            else:
                spec_fun = line[space + 1:left - 1]
            str_spec_fun = spec_fun.strip().split()  # 将物种、功能一起的混合字符串按照空格切分
            part2 = str_spec_fun[0] + " " + str_spec_fun[1]  # 提取到物种！！
            part3 = ""
            for num in range(2, len(str_spec_fun)):  # 提取2到最后一个位置的内容，作为功能
                i = str_spec_fun[num]
                part3 = part3 + " " + i
            part3 = part3.strip()  # 至此找完part3即功能列
            gid = part1  # 定义gid,用于接收基因名称（也就是part1 ）作为主键
            species[gid] = part2
            gene[gid] = part1
            func[gid] = part3
        else:
            sub_seq = line.strip().split()
            strseq0 = ''.join(sub_seq)
            strseq = strseq0.replace('\n', '')
            if gid in seq.keys():  # 判断字典键值(gid基因)是否已存在
                seq[gid] = seq[gid] + strseq  # 字典的值拼接
            else:
                seq[gid] = strseq
    fcds.close()
    # print('\n基因序列表数据为:')
    # for gid in gene.keys():
    #     print(species[gid] + "\t" + gene[gid] + "\t" + func[gid] + "\t" + seq[gid])

    # # 保存字典到文件(将读取到的有用信息写入基因序列表（Gene_seq），得到对应列的内容：物种名，基因名，功能，序列)
    for gid in gene.keys():
        fseq = [species[gid], gene[gid], func[gid], seq[gid]]
        with open(table_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fseq)


# ###pfam.out文件：———基因结构信息表（Gene_struc）：物种名，基因名，包含结构名，结构ID
def out(out_file_path, specName, table_path):
    fout = open(out_file_path, "r")  # 以读方式打开out文件
    species = specName  # 物种
    gene = {}  # 结构基因字典，对应pfam文件
    struID = {}  # 结构ID字典
    struName = {}  # 结构名称字典
    for line_stru in fout.readlines():
        if line_stru.startswith('Acera_'):
            col_stru = line_stru.strip().split()
            sGene = col_stru[0][6:]  # 至此找完基因名称列
            gid = sGene  # 字符串gid,用于接收基因名称作为主键！！
            ID = col_stru[5]  # 至此找完结构ID列
            Name = col_stru[6]  # 至此找完结构名称列
            gene[gid] = sGene
            struID[gid] = ID  # 结构ID字典
            struName[gid] = Name  # 结构名称字典
    # print('\n基因结构表数据为:\n','species'+'\t'+'gene'+'\t'+'struID'+'\t'+'struName')
    # for gid in gene.keys():
    #     print(species+'\t'+gene[gid] + "\t" + struID[gid] + "\t" + struName[gid])

    # # 保存字典到文件(将读取到的有用信息写入基因结构信息表（Gene_struc）：物种名，基因名，包含结构名，结构ID)
    for gid in gene.keys():
        fstru = [species, gene[gid], struID[gid], struName[gid]]
        with open(table_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fstru)


# ##gff文件：———基因位置信息表（Gene_loc）：物种名，基因名,染色体名，起始位点，终止位点，基因方向
def gff(gff_file_path, specName, table_path):
    fgff = open(gff_file_path, "r")  # 以读方式打开gff文件
    species = specName  # 物种
    chrom = {}  # 结构染色体名字典，对应gff文件
    gene = {}  # 基因字典
    start = {}  # 起始位点字典
    end = {}  # 终止位点
    direc = {}  # 基因方向
    for line_loc in fgff.readlines():
        if line_loc.startswith('N'):
            col_loc = line_loc.strip().split()
            RNA = col_loc[2]
            if RNA.endswith("RNA"):  # 找到拥有(.*)RNA，找到对应的染色体名,以及基因名称，例如“Name=NM_001328477.1”
                chromosome = col_loc[0]  # 至此找完染色体名称列
                locStart = col_loc[3]  # 至此找完起始位点列
                locEnd = col_loc[4]  # 至此找完终止位点列
                direction = col_loc[6]  # 此处开始找基因方向列
                if '+' in direction:  # 判断是否为正向“+”
                    direction = '+'
                elif '-' in direction:  # 判断是否为反向“-”
                    direction = '-'
                else:  # 既非正向+，也非反向-，方向未知“.”
                    direction = '.'
                geneStr = col_loc[8]  # 此处找到含有基因名称的长字符串
                if "Name=" in geneStr:
                    fenhao = geneStr.find(";")  # 分号第一次出现的位置
                    fenhao2 = geneStr.find(";", fenhao + 1)  # 第二次出现的位置
                    fenhao3 = geneStr.find(";", fenhao2 + 1)  # 第三次出现的位置
                    fenhao4 = geneStr.find(";", fenhao3 + 1)  # 第四次出现的位置
                    ##提取第三个分号与第四次位置之间（即;Name=XM_017066638.2;），找到基因名
                    geneName = geneStr[fenhao3 + 6:fenhao4]
                gid = geneName  # 字符串gid,用于接收基因名称作为主键
                chrom[gid] = chromosome  # 结构染色体名字典，对应gff文件
                gene[gid] = geneName  # 基因名字典
                start[gid] = locStart  # 起始位点字典
                end[gid] = locEnd  # 终止位点
                direc[gid] = direction  # 基因方向
    fgff.close()
    # print('\n基因位置表数据为:\n','species'+'\t'+'gene'+'\t'+'chromosome'+'\t'+'start'+'\t'+'end'+'\t'+'direction')
    # for gid in gene.keys():
    #     print(species + "\t" + gene[gid] + "\t" + chrom[gid] + '\t' + start[gid] + '\t' + end[gid] + '\t' + direc[gid])

    # # 保存字典到文件(将读取到的有用信息写入基因位置信息表（Gene_loc）：物种名，基因名,染色体名，起始位点，终止位点，基因方向
    for gid in gene.keys():
        floc = [species, gene[gid], chrom[gid], start[gid], end[gid], direc[gid]]
        with open(table_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(floc)


# ###获取不同类型文件的绝对路径
# root:当前目录路径，dir:当前路径下所有子目录，file:当前路径下所有非目录子文件
def file_path(file_dir):
    cds_file_path = []  # cds文件列表，包含五个物种的cds文件，从中获得基因序列表
    out_file_path = []  # out文件列表
    gff_file_path = []  # gff文件列表
    specName = []  # 物种名列表
    for root, dir, file in os.walk(file_dir):
        for file1 in file:
            if (re.match(r'(.*).cds', file1)):
                cdsStr = (root + '/' + file1).replace('\\', '/')
                cds_file_path.append(cdsStr)
            elif (re.match(r'(.*).out', file1)):
                outStr = (root + '/' + file1).replace('\\', '/')
                out_file_path.append(outStr)
            elif (re.match(r'(.*).gff', file1)):
                gffStr = (root + '/' + file1).replace('\\', '/')
                gff_file_path.append(gffStr)
    for i in range(0, len(cds_file_path)):  # 循环找到/位置，以此截取到物种名称，放到物种列表里
        spec = cds_file_path[i]
        xie = spec.find("/")  # “/”第一次出现的位置
        xie2 = spec.find("/", xie + 1)  # 第二次出现的位置
        xie3 = spec.find("/", xie2 + 1)  # 第三次出现的位置
        xie4 = spec.find("/", xie3 + 1)  # 第四次出现的位置
        xie5 = spec.find("/", xie4 + 1)  # 第五次出现的位置
        # 提取第四个斜线与第五次位置之间（例如：/Apis_cerana/），找到物种名
        speciesName = spec[xie4 + 1:xie5]
        specName.append(speciesName)
    return cds_file_path, out_file_path, gff_file_path, specName


if __name__ == '__main__':
    paths = file_path('E:/A`毕业设计/蜜蜂数据处理/蜜蜂/')
    # print(paths)  #得到([cds文件列表],[out文件列表],[gff文件列表],[物种列表])，对应seq、stru、loc
    # ##1.指定基因序列表（Gene_seq）的保存路径,2.基因结构表（Gene_struc）,3.基因位置信息表（Gene_loc）
    cds_to_seq_path = 'E:/A`毕业设计/蜜蜂数据处理/蜜蜂test/数据表test/Gene_seq.csv'
    out_to_stru_path = 'E:/A`毕业设计/蜜蜂数据处理/蜜蜂test/数据表test/Gene_struc.csv'
    gff_to_loc_path = 'E:/A`毕业设计/蜜蜂数据处理/蜜蜂test/数据表test/Gene_loc.csv'

    # ##用数组表示要写入的一行内容，将列名先定义好，基因序列表（Gene_seq）：物种名，基因名，功能，序列
    # #基因序列表（Gene_seq）：物种名，基因名，功能，序列
    # #基因位置信息表（Gene_loc）:物种名，基因名, 染色体名，起始位点，终止位点，基因方向
    fseq_column = ['species', 'gene', 'function', 'seq']
    fstru_column = ['species', 'gene', 'struID', 'struName']
    floc_column = ['species', 'gene', 'chromosome', 'gstart', 'gend', 'direction']

    # 打开文件,打开模式为追加模式‘a’时，如果文件不存在，系统会自动创建文件,newline可避免空行
    fseq = open(cds_to_seq_path, 'a', newline='')
    content = csv.writer(fseq, dialect='excel')  # 设定文件写入模式
    content.writerow(fseq_column)  # 将列名写入写入具体内容

    fstru = open(out_to_stru_path, 'a', newline='')  # 追加模式打开
    content = csv.writer(fstru, dialect='excel')  # 设定文件写入模式
    content.writerow(fstru_column)  # 将列名写入写入具体内容

    floc = open(gff_to_loc_path, 'a', newline='')  # 追加模式打开
    content = csv.writer(floc, dialect='excel')  # 设定文件写入模式
    content.writerow(floc_column)  # 将列名写入写入具体内容

    for cdsi in range(0, len(paths[0])):  # 0-遍历所有的cds文件
        gene_seq = cds(cds_file_path=paths[0][cdsi], table_path=cds_to_seq_path)  # 得到基因序列表
        # print(paths[0][cdsi])
    for outi in range(0, len(paths[1])):  # 对应1，遍历所有的out文件
        for specj in range(0, len(paths[3])):  # 对应3，遍历所有的物种名称，传给基因结构表
            gene_stru = out(out_file_path=paths[1][outi], specName=paths[3][specj],
                            table_path=out_to_stru_path)  # 得到基因结构表
        # print(paths[1][outi])
    for gffi in range(0, len(paths[2])):  # 2-遍历所有的gff文件
        for specj in range(0, len(paths[3])):  # 遍历所有的物种名称，传给基因结构表
            gene_loc = gff(gff_file_path=paths[2][gffi], specName=paths[3][specj],
                           table_path=gff_to_loc_path)  # 得到基因位置表
        # print(paths[2][gffi])
    out_path = 'saveDate'
    start_time = time.time()
    end_time = time.time()
    print("Total Running time:%.4f s" % (end_time - start_time))
    save_log("Total Running time:%.4f s" % (end_time - start_time))
