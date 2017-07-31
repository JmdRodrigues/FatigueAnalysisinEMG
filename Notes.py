from PlottingSavers import PlotRadar

def TestFunction():
    data = [[['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [371.95769929581945, 436.74483791677886, 731.36419414320073,
                                               858.37666564673987, 1271.5716012639075, 1386.6464465465299,
                                               958.63646874180677, 972.0388854523967, 1192.9668470174615,
                                               1394.8159963072085]), ('Vastus_Lateralis',
                                                                      [720.79905238794902, 839.68783079812954,
                                                                       1036.8502946497952, 1062.8283006721974,
                                                                       1065.1895323404158, 1994.8838032571778,
                                                                       1758.3397114735058, 1314.8635142199744,
                                                                       1594.1470956000976, 1764.2282292287757]), (
             'Vastus_Medialis',
             [73.990497221489662, 75.775246778294004, 100.49122864178365, 129.60978448719931, 107.55703360942766,
              132.4547425314214, 165.54839291517044, 91.198562345513693, 84.694533057920651, 126.1750400876236]), (
             'SemiTendinosus',
             [78.003002870852967, 104.68922516834155, 88.095581446390511, 112.80078778846331, 142.85155603402211,
              109.06100353789724, 132.58267892918605, 175.3002738008731, 171.34823913917697, 488.89350940801876]), (
             'Biceps_Femoris',
             [26.408663126402189, 17.735346846256437, 15.868534023361303, 17.227749298291386, 15.047666931827552,
              21.095335758891984, 24.325251325398693, 20.391428472632199, 18.964412772064264, 19.643265347343924])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [82.934848931925359, 162.59525287877506, 165.22282791255356,
                                               202.38109805235283, 192.73341556447696, 249.01577623929728,
                                               332.40604953139444, 355.18553616122301, 394.14047493819993,
                                               397.60295033986569]), ('Vastus_Lateralis',
                                                                      [252.69600881190027, 339.17768468460946,
                                                                       450.99984473840692, 418.72058890493906,
                                                                       397.1028859004561, 428.46397109444291,
                                                                       697.10886822609973, 488.36937845015808,
                                                                       843.2742304509344, 881.29195622068085]), (
             'Vastus_Medialis',
             [98.361939661011078, 142.678333679095, 138.41913431342695, 156.12713608258301, 241.05276046172807,
              222.00968696160345, 160.41716728029706, 181.50291013612244, 185.77356526684972, 254.68265737715657]), (
             'SemiTendinosus',
             [169.13496841860263, 304.14763250969713, 286.52200492531307, 228.62957776403218, 179.43154277942193,
              280.14781642616504, 349.15085275420728, 434.25702893923005, 490.13578586409881, 538.00718020247143]), (
             'Biceps_Femoris',
             [41.220709067911422, 45.770331231013998, 38.234429795656119, 40.085317544938363, 34.638645561422976,
              38.584432533219761, 38.466084856794247, 32.079886714118238, 38.47311263637522, 52.592173224096015])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [116.59904383864558, 136.61397058564916, 395.97513960358822,
                                               527.8569623066395, 626.35919943962142, 704.6966484191023,
                                               809.26163350679917, 648.93172776220206, 601.45960347746609,
                                               567.38277212800608]), ('Vastus_Lateralis',
                                                                      [617.00605200956454, 663.5116982664581,
                                                                       964.30082732782751, 1414.5972921097032,
                                                                       1286.2516527393395, 1087.9243429401506,
                                                                       1841.1194953693816, 1493.3766715648997,
                                                                       1600.9873346084062, 1595.5869842135264]), (
             'Vastus_Medialis',
             [19.764376626376674, 25.048635562696653, 26.453300056609791, 32.963562730255845, 26.340784978886045,
              36.66015022565211, 40.575695292875672, 35.122435043694566, 40.318495517041285, 94.538481662548548]), (
             'SemiTendinosus',
             [265.63937927651165, 314.55505037646583, 273.57646777782929, 225.2100335495046, 187.04770365385286,
              161.73743871785874, 164.40229055140054, 205.49981016232041, 250.05841908819454, 161.29957490565687]), (
             'Biceps_Femoris',
             [94.562647931874181, 69.255392822974358, 72.789117858550298, 67.064065250782178, 75.19970601653759,
              84.759877727237679, 65.097477112691934, 97.529435399197084, 108.6402301427087, 83.787285906829879])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [120.28016599778194, 255.0107672491107, 320.4463949333196,
                                               479.90596804455248, 590.72389409245989, 403.23650888183857,
                                               362.75893425056586, 488.81182276072002, 361.099836788743,
                                               307.48043684329235]), ('Vastus_Lateralis',
                                                                      [139.98802323380301, 123.12781263119551,
                                                                       202.20795270590332, 349.98505066975957,
                                                                       468.19430556004102, 654.71629771545236,
                                                                       740.8772826294321, 1020.1330700031161,
                                                                       1034.5481519742316, 911.8724203844796]), (
             'Vastus_Medialis',
             [413.03735022618349, 431.92700900114482, 339.40863784644563, 301.2698737767019, 261.83158634695866,
              109.63484487610579, 109.80167435439091, 200.66444638755357, 187.50950281172868, 126.72252263825141]), (
             'SemiTendinosus',
             [323.75056481625228, 525.7663812208142, 474.98634601923999, 287.39954274176631, 273.57690228054679,
              269.9983144142833, 235.43942890218162, 196.66953745116521, 225.76715986811294, 287.68598394365011]), (
             'Biceps_Femoris',
             [127.86059706699918, 138.22147079326547, 119.87449443426902, 118.32667760585437, 57.232093936246343,
              57.834041184858187, 52.572902177117498, 49.555192992417879, 57.188114668594913, 65.672462648021607])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [98.029448489040774, 213.98342756837917, 224.93445184718405,
                                               297.54696563337865, 400.75319542871347, 437.9760671147971,
                                               603.00543040918205, 595.03079095962335, 328.44085498152623,
                                               2.4271112072810439]), ('Vastus_Lateralis',
                                                                      [388.28800108991709, 704.06422588817077,
                                                                       814.2964321049792, 943.26966584858815,
                                                                       950.091300050222, 834.8940976972948,
                                                                       859.56531456999221, 1132.5295939272387,
                                                                       580.25416250511057, 4.7181950728867781]), (
             'Vastus_Medialis',
             [136.90338742571049, 201.36619625680331, 254.67011372033403, 201.86995965571148, 202.23629618566571,
              252.63585818267157, 264.91282079643315, 325.60449777609358, 250.53339017286891, 34.160228656766598]), (
             'SemiTendinosus',
             [183.23366786734448, 238.9572365442815, 290.95391305308806, 641.16915089951203, 507.66375003704991,
              403.64598969124199, 554.70715303309089, 374.88341203594018, 148.31293323205907, 0.98923033496768153]), (
             'Biceps_Femoris',
             [95.50588711979367, 132.1065699424239, 135.77183607175635, 128.23761189354133, 148.66214522181198,
              140.07837139552811, 152.18283708659044, 147.76494209542582, 131.43260806069753, 56.40469676795454])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [268.61196503028646, 252.43453614768794, 456.1381559369525,
                                               476.82955695524265, 725.87852391892034, 1193.5764126892279,
                                               2081.4995566550624, 1978.6585778202943, 1700.7392043412819,
                                               1563.943695145234]), ('Vastus_Lateralis',
                                                                     [1163.0777097285991, 1121.0003595027958,
                                                                      1988.1576589946783, 2237.1274400201678,
                                                                      2554.1323969665764, 3522.242220996874,
                                                                      2462.1416791193542, 4061.3226467326735,
                                                                      3152.1330567049099, 3988.6366113991153]), (
             'Vastus_Medialis',
             [166.21437257880609, 188.75654445363898, 218.44028631774185, 226.69638459038407, 315.53387662671747,
              426.67226057957481, 377.89368282280623, 532.18115553202028, 796.8847180774178, 933.26378767279778]), (
             'SemiTendinosus',
             [220.86360451688867, 343.57333279143393, 361.7093713353313, 459.75677618423282, 804.91125035114806,
              1745.4154537636357, 1822.0619154971009, 2864.5561838749568, 3049.1307909612124, 3333.1599960188591]), (
             'Biceps_Femoris',
             [101.96076228565801, 130.99637519285088, 141.84324869425652, 173.17318803509113, 226.47852303617233,
              214.82040365025108, 180.52262942839317, 266.29114876744961, 267.54992041552669, 223.28252685415646])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [72.527397268781201, 123.91635973928393, 255.2572516601669,
                                               253.66040166654503, 448.02456968773998, 751.30375179339023,
                                               1238.8944608247637, 2160.1673659664043, 1901.8837415280764,
                                               1237.6744759613016]), ('Vastus_Lateralis',
                                                                      [849.96513284658556, 1546.3465935662373,
                                                                       1888.9882421504806, 2487.1821430782752,
                                                                       2535.8198804705121, 3570.8475558638602,
                                                                       3350.5649158033025, 5530.118484786075,
                                                                       3932.5909221670909, 5664.8423657217663]), (
             'Vastus_Medialis',
             [1241.5833153825149, 2033.4764187908777, 2241.5475482689708, 1913.9735827057557, 1503.8606871410586,
              1152.4644152904511, 1253.340216989292, 1268.4107831544964, 1356.0518016445421, 1542.9440996182377]), (
             'SemiTendinosus',
             [267.63338822659398, 324.20065268877693, 539.09685033186668, 430.42247951656009, 485.42404369208003,
              552.09764448159615, 648.07353867324639, 528.33982794744679, 684.99839632034445, 798.05129206713059]), (
             'Biceps_Femoris',
             [371.85714430790824, 372.23760510241698, 344.79719251984574, 269.89811480239166, 262.59267137405766,
              294.67237285397289, 375.1585186232216, 380.75612426815167, 348.42419971643557, 344.33575198433124])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [320.73839440213067, 401.7477681788377, 332.38582154203624,
                                               432.14893811049723, 538.47397777741151, 405.4396908441002,
                                               604.10468546547486, 423.34478335399967, 816.58298134210952,
                                               548.40443843093601]), ('Vastus_Lateralis',
                                                                      [511.42097844656149, 724.49290520436637,
                                                                       459.9348471155165, 543.98213215261183,
                                                                       928.70310628263701, 625.69031495615991,
                                                                       530.21253640541909, 586.36531780993846,
                                                                       616.31592522137316, 461.29682867888806]), (
             'Vastus_Medialis',
             [249.09701916057702, 358.60268069053285, 291.70015243614483, 227.16311045511733, 393.91294941893301,
              344.55243392964456, 399.28681219941706, 479.59031951826387, 373.33055954472843, 528.98827502723145]), (
             'SemiTendinosus',
             [301.95735150289369, 454.84910512544735, 416.61420881065811, 591.55520869638838, 662.61809629812308,
              732.04127461458177, 460.86598633765237, 412.15458763288711, 400.11973386439678, 354.77680061662272]), (
             'Biceps_Femoris',
             [387.84658535488893, 1162.7135433431656, 675.51546854037485, 426.41236969403292, 474.62832900830983,
              310.99534546663864, 519.29963539903167, 590.3571703948428, 480.10245018959375, 638.82065861657111])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [50.712279361523528, 47.16286549434421, 41.438193590928272,
                                               79.21760657292937, 81.597169801869612, 62.679665364269987,
                                               75.581125937907771, 89.738700905283153, 110.45637825535348,
                                               108.33750238249215]), ('Vastus_Lateralis',
                                                                      [476.87208614100109, 405.39121931866998,
                                                                       431.26150895016406, 496.67901158118065,
                                                                       346.21541457565831, 495.98607603847842,
                                                                       527.36738345615026, 368.50622863080008,
                                                                       751.51883155069243, 548.34377451969453]), (
             'Vastus_Medialis',
             [29.805670143147371, 34.012500945420491, 42.557216049717276, 44.143363844482913, 44.883653545847189,
              42.390718374374543, 45.567844919610224, 31.76194483375555, 35.229125811521115, 60.509851734793074]), (
             'SemiTendinosus',
             [175.24239242660553, 123.38476874524035, 103.38686910676346, 137.09808985448868, 194.34716516272934,
              197.8415375926472, 147.13277183759865, 133.79299728663969, 121.42748231636988, 257.62568419283741]), (
             'Biceps_Femoris',
             [58.569769989063296, 68.448840789987216, 42.693304171847934, 56.856474887849885, 46.197695347955026,
              52.700317115650165, 59.023661297789097, 61.272313545281868, 53.705254682110926, 68.260625193607169])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [52.217050982345341, 71.622157957535251, 57.872304512562195,
                                               74.591559859768552, 138.77450289541741, 96.7427596186687,
                                               83.387489103280259, 99.509997012973429, 120.35527284285577,
                                               119.50166310112232]), ('Vastus_Lateralis',
                                                                      [189.46786376928449, 416.09760513755907,
                                                                       240.79653894567033, 462.07183468596571,
                                                                       291.2146882852075, 407.1676142267745,
                                                                       436.26933312260951, 338.435875857864,
                                                                       393.53765342594556, 335.59549353606769]), (
             'Vastus_Medialis',
             [28.336105562111104, 28.798479035510084, 37.726261254548277, 35.995696412303296, 73.923682646373663,
              64.861376062865943, 56.574527487443916, 59.555358557273777, 73.744075592825524, 63.21883429560409]), (
             'SemiTendinosus',
             [69.322838222173488, 64.05457961788801, 59.503294110545866, 74.655711238821013, 99.118619546520179,
              126.03914638036326, 88.277077932408218, 122.46180794489889, 139.7918954021824, 141.39961541161969]), (
             'Biceps_Femoris',
             [160.7171051080349, 245.89011740059422, 126.03613234203004, 133.62150711749896, 103.30915105705375,
              111.90796687007908, 142.05350064577766, 155.46246443370882, 109.79402911932719, 87.685042306157897])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [35.271325681827527, 75.13484579931513, 141.4132786003851,
                                               134.83380917328208, 205.38587043765193, 206.44051562465873,
                                               273.78625572000351, 278.91286754193402, 392.77563659104078,
                                               407.21353201643484]), ('Vastus_Lateralis',
                                                                      [186.27711688642754, 268.03962122764449,
                                                                       624.10750353453295, 432.13524920679851,
                                                                       691.74817145059797, 683.28240470182448,
                                                                       649.51896246828437, 895.52122084752159,
                                                                       778.72673518495139, 1324.3789180922759]), (
             'Vastus_Medialis',
             [26.530355250452111, 35.33539772641911, 28.228670769344685, 45.327994762778168, 48.291519257151734,
              37.15168442336104, 38.410264809094912, 56.583468819490882, 41.679066933581943, 53.874842774552683]), (
             'SemiTendinosus',
             [90.300225946782959, 127.62778303017731, 136.2031619446667, 81.473313098505272, 92.165558940910273,
              182.93282064545227, 106.26938382624245, 188.83661872413856, 160.77616927484615, 133.66921596376645]), (
             'Biceps_Femoris',
             [19.97928343401712, 11.782090341081192, 10.6057905432027, 14.466237198117037, 14.236789979544943,
              11.126827196357526, 9.2844117219716029, 17.295512066427108, 14.005143442640934, 16.907027081675068])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [44.862371357657267, 48.170104737532874, 26.791735827094382,
                                               30.555090334261685, 63.979719451653125, 53.020000773353459,
                                               55.327706621560495, 54.430110787508191, 87.147946309909557,
                                               227.01643541954343]), ('Vastus_Lateralis',
                                                                      [60.077956209948916, 71.929940457418795,
                                                                       61.986341424528788, 76.505961696776922,
                                                                       86.993258584875562, 94.760102806348655,
                                                                       91.266749470784333, 89.775845754820736,
                                                                       103.78987333933817, 96.944112223623662]), (
             'Vastus_Medialis',
             [8.7289209593462385, 10.402672802408032, 14.196336604017873, 11.220279327709775, 8.3131764790209814,
              10.617092465849668, 10.975009712150671, 18.513348001732997, 11.376822662993956, 12.653587674531034]), (
             'SemiTendinosus',
             [55.813183196090257, 95.557024329727554, 94.62717427430934, 96.70665785680643, 95.115706686968537,
              109.80475046119933, 87.828027435172018, 64.969596193254134, 86.103305062228685, 77.432355143327598]), (
             'Biceps_Femoris',
             [23.915670539301228, 21.886022049822586, 17.894557096987466, 17.919611865886775, 24.814438390035676,
              19.173070270520707, 10.193320676274316, 7.2947123906929043, 7.38428156576974, 8.7957618961239099])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [118.12474230452487, 267.16575125238882, 349.79251220292809,
                                               721.54933515537687, 924.11451563977812, 800.98365208890186,
                                               678.83368380523132, 760.24847727678218, 712.61156617638301,
                                               721.99602815656203]), ('Vastus_Lateralis',
                                                                      [1702.290755245195, 2881.7793959353271,
                                                                       4459.6251416522318, 4451.2194058803598,
                                                                       4291.3598151186234, 5529.0284277295923,
                                                                       4788.7868320093839, 5100.9612447248937,
                                                                       5636.7733797159262, 4133.0754690795638]), (
             'Vastus_Medialis',
             [46.078707558706633, 92.303614640926469, 130.75615628486673, 122.67300251842065, 80.109708658110634,
              157.40148446565325, 239.50004069511809, 257.75548743543936, 211.34562094761847, 189.33278428461185]), (
             'SemiTendinosus',
             [222.68425549545566, 398.27447827408434, 417.45922734433344, 552.94482873117352, 691.6190364789536,
              727.41702132923217, 712.93590011147762, 848.77045154857501, 1064.7047847517986, 1459.8228070073087]), (
             'Biceps_Femoris',
             [25.027856728550198, 9.2051684814427084, 12.266236249548514, 15.015987513756667, 15.584595293906588,
              25.177580150234803, 30.1006131030021, 33.622971393781107, 24.303311111098598, 54.941138098884053])],
            [['RF', 'VL', 'VM', 'ST', 'BF'], ('Rectus_Femoris',
                                              [32.876054903903835, 28.997983051841732, 54.553444639742743,
                                               73.123654262514648, 103.13626229901259, 153.34997086986073,
                                               258.61871288425914, 264.86416794497745, 352.25361905610185,
                                               268.39079138950416]), ('Vastus_Lateralis',
                                                                      [121.16192372498958, 178.30447705466574,
                                                                       169.15650459442006, 225.61913320250619,
                                                                       253.82404616931061, 262.32450364938791,
                                                                       329.82663537544317, 561.9430332671609,
                                                                       438.39855733429681, 386.65844632761019]), (
             'Vastus_Medialis',
             [14.900918580309147, 10.015669789828795, 6.7057764438244574, 6.5901830853236438, 13.20063008390358,
              5.4866363437240819, 16.332611053243493, 13.351574688900127, 10.648335524816183, 11.710326223495136]), (
             'SemiTendinosus',
             [78.81880872350483, 84.419787036432439, 63.03792755470355, 92.78070853337357, 92.521377700361398,
              103.03691661321932, 104.36000610306093, 94.570303159821194, 99.393350899359433, 48.135624796674882]), (
             'Biceps_Femoris',
             [41.535453034562018, 33.616930150871021, 21.273603615700956, 29.001819041465019, 41.753876159552505,
              40.440407230747866, 42.763665878794697, 31.973139727245265, 37.905856666596677, 21.73536605027077])]]

    sbjOrder = ['Subject10', 'Subject11', 'Subject12', 'Subject13', 'Subject14', 'Subject15', 'Subject2', 'Subject3',
                'Subject4', 'Subject5', 'Subject6', 'Subject7', 'Subject8', 'Subject9']

    PlotRadar(data, sbjOrder)

# Radar Chart Test 1.

# PlotRadar(dataRep, ['Sbj10', 'Sbj15', 'Sbj2', 'Sbj3', 'Sbj4', 'Sbj5', 'Sbj6', 'Sbj7', 'Sbj8', 'Sbj9'])

# # Radar Chart Test 0.
#
# nbrMuscles = 5
# theta = radar_factory(nbrMuscles, frame='polygon')
#
# data = example_data()
# #print (data)
# print (data)
# # print ((data[1][1][:][1]))
# # print (data[1:][:][1][1])
# #
# # print ("len(data[1])")
# # print (len(data[1][1]))
# # print (data[1][1][3])
# data[0] = data[0][:5]
#
# #print (len(data[1:]))
# #print (data[1:])
#
# for i in range(1, len(data[1:]) + 1):
# 	for j in range(0, len(data[1][1])):
# 		data[i][1][j] = data[i][1][j][:5]
#
#
# #labelsMscName = ['Rectus_Femoris', 'Vastus_Lateralis', 'Vastus_Medialis', 'SemiTendinosus', 'Biceps_Femoris', '', '', '', '']
# labelsMscName = data.pop(0)
# # Generation of a figure with five rows.
# fig, axes = plt.subplots(nrows=1, ncols=1, subplot_kw=dict(projection='radar'))
# fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
#
# #print (axes.flatten(), data)
#
# colors = ['b', 'r', 'g', 'm', 'y']
# # Plot the four cases from the example data on separate axes
# # for ax, (title, case_data) in zip(axes.flatten(), data):
# #         ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
# #         ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1), horizontalalignment='center', verticalalignment='center')
# #         for d, color in zip(case_data, colors):
# #             ax.plot(theta, d, color=color)
# #             ax.fill(theta, d, facecolor=color, alpha=0.25)
# #         ax.set_varlabels(labelsMscName)
# #
# # # add legend relative to top-left plot
# # ax = axes[0, 0]
# # labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
# # legend = ax.legend(labels, loc=(0.9, .95), labelspacing=0.1, fontsize='small')
#
# axes.set_rgrids([0.2, 0.4, 0.6, 0.8])
# axes.set_title('A', weight='bold', size='medium', position=(0.5, 1.1), horizontalalignment='center', verticalalignment='center')
# #print (data[1][1])
#
# for d, color in zip(data[1][1], colors):
# 	axes.plot(theta, d, color=color)
# 	axes.fill(theta, d, facecolor=color, alpha=0.25)
# axes.set_varlabels(labelsMscName)
#
# # add legend relative to top-left plot
# #ax = axes[0, 0]
# labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
# legend = axes.legend(labels, loc=(0.9, .95), labelspacing=0.1, fontsize='small')
#
# fig.text(0.5, 0.965, '5-Factor Solution Profiles Across Four Scenarios', horizontalalignment='center', color='black', weight='bold', size='large')
#
# plt.show()




# ----------------------------------------------------------------------------------------------------------------------

# --------------------------------- Old Version of Analyis Function ----------------------------------------------------

# EMG Signal Analysis - Nuclear Function.
# def Analysis(filename, path, signal, pks_start, pks_end, fs, wavelet, txt_data_temp, txt_data_global, pandaData,
#              final=False):
#     # [NOTE] The txt_data_global array will be used for a txt file generation with the results of the different Analysis.
#
#     # ----- Copy of content. -----
#     # (Is needed to preserve the original information between iterations. We change the array txt_data_temp
#     # and in any moment the original content can be retrieved with txt_data_aux).
#     txt_data_aux = list(txt_data_temp)
#
#     # ---- PreProcessing EMG -----
#     emg = EMG_Pre_P(signal, fs)
#
#     # Calculate Scalogram
#     frequencyRange = np.arange(5, 500, 4)
#     # frequencyRange = np.arange(5, 500, 1) # Memory Error.
#     scales = 1000 * freq2scale(frequencyRange, wavelet)
#
#     # Time to Frequency Domain Transposition.
#     coef, freqs = pywt.cwt(emg, scales, wavelet, sampling_period=1.0 / fs)
#
#     # Calculate meanBurstsParameters
#     cwt_N = CreateInterpolatedBurstCWT(coef, pks_start, pks_end)
#
#     # Report Specifications.
#     PDFName = filename + '.pdf'
#
#     if not os.path.exists(path + "/" + PDFName[:-4]):
#         os.makedirs(path + "/" + PDFName[:-4])
#
#     # ----- Analysis 1 - Burst to Burst Analysis. -----
#     print("The Analysis1 started. [Burst by Burst Processing]")
#     pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis1_" + PDFName)
#
#     plotEMG(pks_start, pks_end, emg, pp)
#     # plotEMG3D(np.power(coef, 2), pp)
#
#     # Analysis of the signal for each burst
#     Analysis1(cwt_N, path, filename, pp)
#
#     pp.close()
#
#     # ----- Analysis 2 - Analysis of the signal using a sliding window mechanism (with or without overlap). ------
#     print("The Analysis2 started. [Restrictive OTSU Thresholding]")
#     pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis2_" + PDFName)
#
#     # -- Original Analysis (window length = 10 and lag = 9) --
#     txt_data_global = Analysis2_4(cwt_N, 10, path, filename, pp, "Original_Analysis", analysis=2,
#                                   txt_data=txt_data_temp, txt_data_global=txt_data_global)
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     # -- Non Overlap Analysis (window length determined with percentile) --
#     length_perc = int(0.10 * len(cwt_N))
#     # The txt_data_global array will be used for a txt file generation with the results of the different Analysis.
#     txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Non_Overlap_Analysis", analysis=2,
#                                   txt_data=txt_data_temp, txt_data_global=txt_data_global)
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     # -- Overlap Analysis (lag = 0.30 or 0.50 or 0.70 of window length) --
#     # [Lag Factor --> 0.70]
#     txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis",
#                                   lag=int(0.70 * length_perc), analysis=2, txt_data=txt_data_temp,
#                                   txt_data_global=txt_data_global)
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     # [Lag Factor --> 0.50]
#     txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis",
#                                   lag=int(0.50 * length_perc), analysis=2, txt_data=txt_data_temp,
#                                   txt_data_global=txt_data_global)
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     # [Lag Factor --> 0.30]
#     txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis",
#                                   lag=int(0.30 * length_perc), analysis=2, txt_data=txt_data_temp,
#                                   txt_data_global=txt_data_global)
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     pp.close()
#
#     # ----- Analysis 3 - Analysis of the beginning and the end of the signal. -----
#     print("The Analysis3 started. [Analysis of the first and last sets of 20 and 50 muscular activation periods]")
#     pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis3_" + PDFName)
#
#     # Sets of 20 Muscular Activations.
#     Analysis3(cwt_N, 20, path, filename, pp)
#     # Sets of 50 Muscular Activations.
#     Analysis3(cwt_N, 50, path, filename, pp)
#
#     pp.close()
#
#     # ----- Analysis 4 - Analysis of the original cwt_map, without OTSUs Thresholds (Identical to Analysis 2). -----
#     print("The Analysis4 started. [Parameters extracted from the original Scalogram]")
#     pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis4_" + PDFName)
#
#     # -- Original Analyis (window length = 10 and lag = 9) --
#     txt_data_global = Analysis2_4(cwt_N, 10, path, filename, pp, "Original_Analysis", analysis=4,
#                                   txt_data=txt_data_temp, txt_data_global=txt_data_global)
#
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     # -- Non Overlap Analyis (window length determined with percentile) --
#     length_perc = int(0.10 * len(cwt_N))
#     txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Non_Overlap_Analysis", analysis=4,
#                                   txt_data=txt_data_temp, txt_data_global=txt_data_global)
#
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     # -- Overlap Analysis (lag = 0.30 or 0.50 or 0.70 of window length) --
#     # [Lag Factor --> 0.70]
#     txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis",
#                                   lag=int(0.70 * length_perc), analysis=4, txt_data=txt_data_temp,
#                                   txt_data_global=txt_data_global)
#
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     # [Lag Factor --> 0.50]
#     txt_data_global, pandaData = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis",
#                                              lag=int(0.50 * length_perc), analysis=4, txt_data=txt_data_temp,
#                                              txt_data_global=txt_data_global, pandaData=pandaData, final=final)
#
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     # [Lag Factor --> 0.30]
#     txt_data_global = Analysis2_4(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis",
#                                   lag=int(0.30 * length_perc), analysis=4, txt_data=txt_data_temp,
#                                   txt_data_global=txt_data_global)
#
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     pp.close()
#
#     # ----- Analysis 5 - Analysis of the cwt_map, with OTSUs Thresholds (But less restrictive than Analysis 2). -----
#     print("The Analysis5 started. [Less Restrictive OTSU Thresholding comparing to Analysis2]")
#     pp = PdfPages(path + "/" + PDFName[:-4] + "/" + "Analysis5_" + PDFName)
#
#     # -- Original Analyis (window length = 10 and lag = 9) --
#     txt_data_global = Analysis5(cwt_N, 10, path, filename, pp, "Original_Analysis", analysis=5, txt_data=txt_data_temp,
#                                 txt_data_global=txt_data_global)
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     # -- Non Overlap Analyis (window length determined with percentile) --
#     length_perc = int(0.10 * len(cwt_N))
#     txt_data_global = Analysis5(cwt_N, length_perc, path, filename, pp, "Non_Overlap_Analysis", analysis=5,
#                                 txt_data=txt_data_temp, txt_data_global=txt_data_global)
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     # -- Overlap Analysis (lag = 0.30 or 0.50 or 0.70 of window length) --
#     # [Lag Factor --> 0.70]
#     txt_data_global = Analysis5(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis", lag=int(0.70 * length_perc),
#                                 analysis=5, txt_data=txt_data_temp, txt_data_global=txt_data_global)
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     # [Lag Factor --> 0.50]
#     txt_data_global = Analysis5(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis", lag=int(0.50 * length_perc),
#                                 analysis=5, txt_data=txt_data_temp, txt_data_global=txt_data_global)
#     # Reboot of content.
#     txt_data_temp = list(txt_data_aux)
#
#     # [Lag Factor --> 0.30]
#     txt_data_global = Analysis5(cwt_N, length_perc, path, filename, pp, "Overlap_Analysis", lag=int(0.30 * length_perc),
#                                 analysis=5, txt_data=txt_data_temp, txt_data_global=txt_data_global)
#
#     pp.close()
#
#     # Synthesis Reports Generation.
#     if final == True:
#         pp = PdfPages(path + "/" + "Synthesis.pdf")
#
#         # Generation of data frame.
#         pandaStruct = DataFrame(np.transpose(pandaData),
#                                 columns=['Subject', 'Muscle', 'Parameter_Name', 'Parameter_Value',
#                                          'Number_of_Burst_Set'])
#
#         # Graphical Representation and fill of data frame.
#         SynthesisGrid(pandaStruct, pp)
#
#         pp.close()
#
#         return txt_data_global, [[], [], [], [], []]
#
#     else:
#         return txt_data_global, pandaData

# ------------------------------------------ Old Version of Grid Plot. -------------------------------------------------

# def SynthesisGridMuscles(pandaData, pp, colIn="PName", rowIn="Msc"):
#     # Identification of the list of muscles.
#     muscleList = list(set(pandaData['Msc'].tolist()))
#
#     # Generation of a pdf synthesis for each muscle.
#     for muscle in range(0, len(muscleList)):
#         pandaTemp = pandaData[pandaData.Msc == muscleList[muscle]]
#
#         # print (pandaData)
#         # Style Configuration.
#         # fig1 = plt.figure()
#         sns.set(style="ticks", color_codes=True)
#
#         # Data Conversion (Work Around because of conversion of int to string when the panda data is created).
#         pandaTemp['#Set'] = pandaTemp['#Set'].astype('int')
#         pandaTemp['PValue'] = pandaTemp['PValue'].astype('float64')
#         maxTime = np.max(pandaTemp['#Set'])
#
#         # Analysis per Subject - Data Frame Creation.
#         dataFrame = sns.FacetGrid(pandaTemp, col=colIn, row=rowIn, sharex=False, sharey=False)
#         # dataFrame.map(sns.pointplot, 'Number_of_Burst_Set', 'Parameter_Value')
#         # dataFrame = dataFrame.map(plt.scatter, "#Set", "PValue")
#         # dataFrame = dataFrame.map(sns.pointplot, "#Set", "PValue", scale=0.3).set(xticks=list(np.arange(0, maxTime + 2, 2)))
#         dataFrame = dataFrame.map(sns.regplot, "#Set", "PValue").set(xticks=list(np.arange(0, maxTime + 2, 2)))
#
#         # Legend Text.
#         figText = plt.figure()
#         plt.text(0, 0,
#                  'Legend' + '\n\n' + '----- Muscles (Msc) -----' + '\n' + '\tRF - Rectus Femoris\n\tVL - Vastus Lateralis\n\tVM - Vastus Medialis\n\tST - Semitendinosus\n\tBF - Biceps Femoris\n\n' + '----- Parameters (PName) ----- ' + '\n\tMF - Major Frequency\n\tMP - Mean Power\n\tCP - Centroid Position\n\tAP - Area in Pixels\n\t CHA - Convex Hull Area\n\tCHV - Convex Hull Volume\n\tTD - Time Dispersion\n\tFD - Frequency Dispersion\n\n' + 'Note ---> [Some indexes may not be present in the graphical representation]' + '\n\n')
#         plt.axis('off')
#
#         pp.savefig(dataFrame.fig)
#         pp.savefig(figText)
