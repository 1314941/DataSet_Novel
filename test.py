from Gen_DataSet import Gen_Little_Text_Thread,CONFIG,Summary,demo




if __name__ == '__main__':
    CONFIG.set_data_root(data_root='data')

    
    demo.queue()
    demo.launch()

    # Gen_Little_Text_Thread().work("data/input/single")
    # Summary().work("data/input/single")
