#! / usr / bin / python
# - * - pengkodean: utf-8 - * -
"" "
Modul ini mengimplementasikan deteksi komunitas.
"" "
__all__  = [ "partition_at_level" , "modularity" , "best_partition" , "generate_dendogram" , "induced_graph" ]
__author__  =  "" "Thomas Aynaud (thomas.aynaud@lip6.fr)" ""
# Hak Cipta (C) 2009 oleh
# Thomas Aynaud <thomas.aynaud@lip6.fr>
# Seluruh hak cipta.
# Lisensi BSD.

__PASS_MAX  =  - 1
__MIN  =  0,0000001

impor  networkx  sebagai  nx
impor  sys
 jenis impor
impor  array


def  partition_at_level ( dendogram , level ):
    "" "Kembalikan partisi dari node pada level tertentu
    Dendogram adalah pohon dan setiap level adalah partisi dari node grafik.
    Level 0 adalah partisi pertama, yang berisi komunitas terkecil, dan yang terbaik adalah len (dendogram) - 1.
    Semakin tinggi levelnya, semakin besar komunitasnya
    Parameter
    ----------
    dendogram: daftar dikt
       daftar partisi, yaitu kamus di mana kunci i + 1 adalah nilai dari i.
    level: int
       tingkat yang dimiliki [0..len (dendogram) -1]
    Kembali
    -------
    partisi: kamus
       Sebuah kamus di mana kunci adalah node dan nilai adalah himpunan miliknya
    Kenaikan
    ------
    KeyError
       Jika dendogram tidak terbentuk dengan baik atau levelnya terlalu tinggi
    Lihat juga
    --------
    best_partition yang secara langsung menggabungkan partition_at_level dan generate_dendogram untuk mendapatkan partisi dengan modularitas tertinggi
    Contoh
    --------
    >>> G = nx.erdos_renyi_graph (100, 0,01)
    >>> dendo = generate_dendogram (G)
    >>> untuk level dalam jangkauan (len (dendo) - 1):
    >>> cetak "partisi pada level", level, "adalah", partition_at_level (dendo, level)
    "" "
    partisi  =  dendogram [ 0 ]. salinan ()
    untuk  indeks  dalam  rentang ( 1 , level  +  1 ):
        untuk  node , komunitas  dalam  partisi . iteritems ():
            partisi [ node ] =  dendogram [ indeks ] [ komunitas ]
     partisi kembali
    

def  modularitas ( partisi , grafik ):
    "" "Hitung modularitas sebuah partisi dari sebuah grafik
    Parameter
    ----------
    partisi: dikt
       partisi dari node, yaitu kamus di mana kunci adalah node dan nilai komunitas
    grafik: networkx.Graph
       grafik networkx yang didekomposisi
    Kembali
    -------
    modularitas: mengapung
       Modularitas
    Kenaikan
    ------
    KeyError
       Jika partisi bukan merupakan partisi dari semua node grafik
    ValueError
        Jika grafik tidak memiliki tautan
    TypeError
        Jika grafik bukan jaringan x.Graph
    Referensi
    ----------
    .. 1. Newman, MEJ & Girvan, M. Menemukan dan mengevaluasi struktur komunitas dalam jaringan. Review Fisik E 69, 26113 (2004).
    Contoh
    --------
    >>> G = nx.erdos_renyi_graph (100, 0,01)
    >>> part = best_partition (G)
    >>> modularitas (bagian, G)
    "" "
    jika  tipe ( grafik ) ! =  nx . Grafik :
        raise  TypeError ( "Jenis grafik buruk, gunakan hanya grafik tidak berarah" )

    inc  =  dict ([])
    derajat  =  dikt ([])
    tautan  =  grafik . ukuran ( berat = 'berat' )
    jika  tautan  ==  0 :
        meningkatkan  ValueError ( "Grafik tanpa tautan memiliki modularitas yang tidak ditentukan" )
    
    untuk  node  dalam  grafik :
        com  =  partisi [ node ]
        derajat [ com ] =  derajat . get ( com , 0. ) +  grafik . derajat ( node , weight  =  'weight' )
        untuk  tetangga , data  dalam  grafik [ node ]. iteritems ():
            berat  =  data . dapatkan ( "berat" , 1 )
            jika  partisi [ tetangga ] ==  com :
                jika  tetangga  ==  simpul :
                    inc [ com ] =  inc . get ( com , 0. ) +  float ( berat )
                lain :
                    inc [ com ] =  inc . get ( com , 0. ) +  float ( berat ) /  2.

    res  =  0.
    untuk  com  dalam  set ( partisi . nilai ()):
        res  + = ( inc . mendapatkan ( com , 0 ) /  link ) - ( deg . mendapatkan ( com , 0. ) / ( 2. * link )) ** 2
    kembali  res


def  best_partition ( grafik , partisi  =  Tidak ada ):
    "" "Hitung partisi dari node grafik yang memaksimalkan modularitas
    (atau coba ..) menggunakan heuristices Louvain
    Ini adalah partisi dengan modularitas tertinggi, yaitu partisi dendogram tertinggi
    dihasilkan oleh algoritma Louvain.
    
    Parameter
    ----------
    grafik: networkx.Graph
       grafik networkx yang didekomposisi
    partisi: dict, optionnal
       algoritme akan mulai menggunakan partisi node ini. Ini adalah kamus di mana kuncinya adalah simpul mereka dan menghargai komunitas
    Kembali
    -------
    partisi: kamus
       Partisi, dengan komunitas yang dinomori dari 0 hingga jumlah komunitas
    Kenaikan
    ------
    NetworkXError
       Jika grafiknya bukan Eulerian.
    Lihat juga
    --------
    generate_dendogram untuk mendapatkan semua level dekomposisi
    Catatan
    -----
    Menggunakan algoritma Louvain
    Referensi
    ----------
    .. 1. Blondel, VD et al. Terungkapnya komunitas dengan cepat dalam jaringan besar. J. Stat. Mech 10008, 1-12 (2008).
    Contoh
    --------
    >>> #Penggunaan dasar
    >>> G = nx.erdos_renyi_graph (100, 0,01)
    >>> part = best_partition (G)
    
    >>> #Contoh lain untuk menampilkan grafik dengan komunitasnya:
    >>> #lebih baik dengan karate_graph () seperti yang didefinisikan dalam contoh networkx
    >>> #erdos renyi tidak memiliki struktur komunitas yang sebenarnya
    >>> G = nx.erdos_renyi_graph (30, 0,05)
    >>> #pertama menghitung partisi terbaik
    >>> partisi = community.best_partition (G)
    >>> #menarik
    >>> ukuran = float (len (set (partition.values ​​())))
    >>> pos = nx.spring_layout (G)
    >>> hitung = 0.
    >>> untuk com dalam set (partition.values ​​()):
    >>> hitung = hitung + 1.
    >>> list_nodes = [node untuk node di partition.keys ()
    >>> jika partisi [node] == com]
    >>> nx.draw_networkx_nodes (G, pos, list_nodes, node_size = 20,
                                    node_color = str (hitungan / ukuran))
    >>> nx.draw_networkx_edges (G, pos, alpha = 0,5)
    >>> plt.show ()
    "" "
    dendo  =  generate_dendogram ( grafik , partisi )
    return  partition_at_level ( dendo , len ( dendo ) -  1 )


def  generate_dendogram ( grafik , part_init  =  Tidak ada ):
    "" "Temukan komunitas dalam grafik dan kembalikan dendogram terkait
    Dendogram adalah pohon dan setiap level adalah partisi dari node grafik. Level 0 adalah partisi pertama, yang berisi komunitas terkecil, dan yang terbaik adalah len (dendogram) - 1. Semakin tinggi levelnya, semakin besar komunitasnya
    Parameter
    ----------
    grafik: networkx.Graph
        grafik networkx yang akan diuraikan
    part_init: dict, optionnal
        algoritme akan mulai menggunakan partisi node ini. Ini adalah kamus di mana kuncinya adalah simpul mereka dan menghargai komunitas
    Kembali
    -------
    dendogram: daftar kamus
        daftar partisi, yaitu kamus di mana kunci i + 1 adalah nilai dari i. dan di mana kunci pertama adalah node dari grafik
    
    Kenaikan
    ------
    TypeError
        Jika grafik bukan jaringan x.Graph
    Lihat juga
    --------
    partisi_baik
    Catatan
    -----
    Menggunakan algoritma Louvain
    Referensi
    ----------
    .. 1. Blondel, VD et al. Terungkapnya komunitas dengan cepat dalam jaringan besar. J. Stat. Mech 10008, 1-12 (2008).
    Contoh
    --------
    >>> G = nx.erdos_renyi_graph (100, 0,01)
    >>> dendo = generate_dendogram (G)
    >>> untuk level dalam jangkauan (len (dendo) - 1):
    >>> cetak "partisi pada level", level, "adalah", partition_at_level (dendo, level)
    "" "
    jika  tipe ( grafik ) ! =  nx . Grafik :
        raise  TypeError ( "Jenis grafik buruk, gunakan hanya grafik tidak berarah" )
    current_graph  =  grafik . salinan ()
    status  =  Status ()
    status . init ( current_graph , part_init )
    mod  =  __modularity ( status )
    status_list  =  daftar ()
    __one_level ( current_graph , Status )
    mod_baru  =  __modularitas ( status )
    partisi  =  __renumber ( status . node2com )
    status_list . tambahkan ( partisi )
    mod  =  new_mod
    current_graph  =  induced_graph ( partisi , current_graph )
    status . init ( grafik_kini )
    
    sementara  Benar :
        __one_level ( current_graph , Status )
        mod_baru  =  __modularitas ( status )
        jika  new_mod  -  mod  <  __MIN :
            istirahat
        partisi  =  __renumber ( status . node2com )
        status_list . tambahkan ( partisi )
        mod  =  new_mod
        current_graph  =  induced_graph ( partisi , current_graph )
        status . init ( grafik_kini )
    kembalikan  status_list [:]


def  induced_graph ( partisi , grafik ):
    "" "Menghasilkan grafik di mana node adalah komunitas
    ada keterkaitan bobot w antar komunitas jika jumlah bobot keterkaitan antar unsurnya adalah w
    Parameter
    ----------
    partisi: dikt
       kamus di mana kuncinya adalah node grafik dan nilai bagian dari node tersebut
    grafik: networkx.Graph
        grafik awal
    Kembali
    -------
    g: networkx.Graph
       grafik networkx di mana node adalah bagian-bagiannya
    Contoh
    --------
    >>> n = 5
    >>> g = nx.complete_graph (2 * n)
    >>> bagian = dikt ([])
    >>> untuk node di g.nodes ():
    >>> bagian [node] = node% 2
    >>> ind = induced_graph (bagian, g)
    >>> tujuan = nx.Graph ()
    >>> nilai_tambahan_bobot_dari ([(0,1, n * n), (0,0, n * (n-1) / 2), (1, 1, n * (n-1) / 2)] )
    >>> nx.is_isomorphic (int, goal)
    Benar
    "" "
    ret  =  nx . Grafik ()
    ret . add_nodes_from ( partisi . nilai-nilai ())
    
    untuk  node1 , node2 , data  dalam bentuk  grafik . edge_iter ( data  =  True ):
        berat  =  data . dapatkan ( "berat" , 1 )
        com1  =  partisi [ node1 ]
        com2  =  partisi [ node2 ]
        w_prec  =  ret . get_edge_data ( com1 , com2 , { "weight" : 0 }). dapatkan ( "berat" , 1 )
        ret . add_edge ( com1 , com2 , weight  =  w_prec  +  weight )
        
     ret kembali


def  __renumber ( kamus ):
    "" "Menomori ulang nilai kamus dari 0 sampai n
    "" "
    hitung  =  0
    ret  =  kamus . salinan ()
    nilai_baru  =  dikt ([])
    
    untuk  kunci  dalam  kamus . kunci ():
        nilai  =  kamus [ kunci ]
        new_value  =  new_values . dapatkan ( nilai , - 1 )
        jika  nilai_baru  ==  - 1 :
            new_values [ value ] =  count
            new_value  =  count
            hitung  =  hitung  +  1
        ret [ key ] =  new_value
        
     ret kembali


def  __load_binary ( data ):
    "" "Muat grafik biner seperti yang digunakan oleh implementasi cpp dari algoritma ini
    "" "
    jika  tipe ( data ) ==  tipe . StringType :
        data  =  terbuka ( data , "rb" )
        
    pembaca  =  larik . larik ( "I" )
    pembaca . fromfile ( data , 1 )
    num_nodes  =  pembaca . pop ()
    pembaca  =  larik . larik ( "I" )
    pembaca . fromfile ( data , num_nodes )
    cum_deg  =  pembaca . daftar ()
    num_links  =  pembaca . pop ()
    pembaca  =  larik . larik ( "I" )
    pembaca . fromfile ( data , num_links )
    tautan  =  pembaca . daftar ()
    grafik  =  nx . Grafik ()
    grafik . add_nodes_from ( range ( num_nodes ))
    prec_deg  =  0
    
    untuk  indeks  dalam  rentang ( num_nodes ):
        last_deg  =  cum_deg [ indeks ]
        tetangga  =  tautan [ prec_deg : last_deg ]
        grafik . add_edges_from ([( indeks , int ( meringkik )) untuk  meringkik  di  tetangga ])
        prec_deg  =  last_deg
        
     grafik kembali


def  __one_level ( grafik , status ):
    "" "Hitung satu tingkat komunitas
    "" "
    modif  =  Benar
    nb_pass_done  =  0
    cur_mod  =  __modularity ( status )
    new_mod  =  cur_mod
    
    sementara  modif   dan  nb_pass_done  ! =  __PASS_MAX :
        cur_mod  =  new_mod
        modif  =  Salah
        nb_pass_done  + =  1
        
        untuk  node  dalam  grafik . node ():
            com_node  =  status . node2com [ node ]
            degc_totw  =  status . gdegrees . get ( node , 0. ) / ( status . total_weight * 2. )
            neigh_communities  =  __neighcom ( node , grafik , status )
            __remove ( node , com_node ,
                    neigh_communities . dapatkan ( com_node , 0. ), status )
            best_com  =  com_node
            peningkatan_baik  =  0
            untuk  com , dnc  di  neigh_communities . iteritems ():
                incr  =   dnc   -  Status . derajat . dapatkan ( com , 0. ) *  degc_totw
                jika  incr  >  best_increase :
                    best_increase  =  incr
                    best_com  =  com                    
            __insert ( node , best_com ,
                    neigh_communities . dapatkan ( best_com , 0. ), status )
            jika  best_com  ! =  com_node :
                modif  =  Benar                
        mod_baru  =  __modularitas ( status )
        jika  new_mod  -  cur_mod  <  __MIN :
            istirahat


 Status kelas :
    "" "
    Untuk menangani beberapa data dalam satu struct.
    Bisa diganti dengan tuple bernama, tetapi tidak ingin bergantung pada python 2.6
    "" "
    node2com  = {}
    total_weight  =  0
    internal  = {}
    derajat  = {}
    gdegrees  = {}
    
    def  __init__ ( diri ):
        diri . node2com  =  dict ([])
        diri . total_weight  =  0
        diri . derajat  =  dikt ([])
        diri . gdegrees  =  dict ([])
        diri . internal  =  dict ([])
        diri . loop  =  dict ([])
        
    def  __str__ ( diri ):
        return ( "node2com:"  +  str ( self . node2com ) +  "derajat:"
            +  str ( self . derajat ) +  "internal:"  +  str ( self . internals )
            +  "total_weight:"  +  str ( self . total_weight ))

    def  copy ( sendiri ):
        "" "Lakukan salinan status" ""
        status_baru  =  Status ()
        status_baru . node2com  =  diri . node2com . salinan ()
        status_baru . internal  =  diri . internal . salinan ()
        status_baru . derajat  =  diri . derajat . salinan ()
        status_baru . gdegrees  =  diri . gdegrees . salinan ()
        status_baru . total_weight  =  diri sendiri . berat keseluruhan

    def  init ( self , graph , part  =  None ):
        "" "Inisialisasi status grafik dengan setiap node dalam satu komunitas" ""
        hitung  =  0
        diri . node2com  =  dict ([])
        diri . total_weight  =  0
        diri . derajat  =  dikt ([])
        diri . gdegrees  =  dict ([])
        diri . internal  =  dict ([])
        diri . total_weight  =  grafik . ukuran ( berat  =  'berat' )
        jika  bagian  ==  Tidak ada :
            untuk  node  dalam  grafik . node ():
                diri . node2com [ node ] =  hitungan
                deg  =  float ( grafik . derajat ( node , weight  =  'weight' ))
                diri . derajat [ hitungan ] =  derajat
                diri . gdegrees [ node ] =  derajat
                diri . loop [ node ] =  float ( grafik . get_edge_data ( node , node ,
                                                 { "berat" : 0 }). dapatkan ( "berat" , 1 ))
                diri . internal [ count ] =  diri . loop [ node ]
                hitung  =  hitung  +  1
        lain :
            untuk  node  dalam  grafik . node ():
                com  =  bagian [ node ]
                diri . node2com [ node ] =  com
                derajat  =  float ( grafik . derajat ( node , timbangan  =  'berat' ))
                diri . derajat [ com ] =  diri . derajat . get ( com , 0 ) +  deg
                diri . gdegrees [ node ] =  derajat
                inc  =  0.
                untuk  tetangga , data  dalam  grafik [ node ]. iteritems ():
                    berat  =  data . dapatkan ( "berat" , 1 )
                    jika  bagian [ tetangga ] ==  com :
                        jika  tetangga  ==  simpul :
                            inc  + =  float ( berat )
                        lain :
                            inc  + =  float ( berat ) /  2.
                diri . internal [ com ] =  diri . internal . get ( com , 0 ) +  inc



def  __neighcom ( node , grafik , status ):
    "" "
    Hitung komunitas di tetangga node dalam grafik yang diberikan
    dengan dekomposisi node2com
    "" "
    bobot  = {}
    untuk  tetangga , data  dalam  grafik [ node ]. iteritems ():
        jika  tetangga  ! =  simpul :
            berat  =  data . dapatkan ( "berat" , 1 )
            neighbourcom  =  status . node2com [ tetangga ]
            bobot [ neighbourcom ] =  bobot . dapatkan ( neighbourcom , 0 ) +  bobot
            
     bobot kembali


def  __remove ( node , com , weight , status ):
    "" "Hapus simpul dari com komunitas dan ubah status" ""
    status . derajat [ com ] = ( status . derajat . get ( com , 0. )
                                    -  status . gdegrees . get ( node , 0. ))
    status . internal [ com ] =  float ( status . internals . get ( com , 0. ) -
                berat  -  status . loop . get ( node , 0. ))
    status . node2com [ node ] =  - 1
    

def  __insert ( node , com , weight , status ):
    "" "Sisipkan simpul ke dalam komunitas dan ubah status" ""
    status . node2com [ node ] =  com
    status . derajat [ com ] = ( status . derajat . get ( com , 0. ) +
                                status . gdegrees . get ( node , 0. ))
    status . internal [ com ] =  float ( status . internals . get ( com , 0. ) +
                        berat  +  status . loop . get ( node , 0. ))


def  __modularity ( status ):
    "" "
    Hitung modularitas partisi grafik menggunakan status precomputed
    "" "
    links  =  float ( status . total_weight )
    hasil  =  0.
    untuk  komunitas  dalam  set ( status . node2com . values ()):
        in_degree  =  status . internal . dapatkan ( komunitas , 0. )
        derajat  =  status . derajat . dapatkan ( komunitas , 0. )
        jika  tautan  >  0 :
            result  =  result  +  in_degree  /  links  - (( derajat  / ( 2. * link )) ** 2 )
     hasil pengembalian


def  __main ():
    "" "Fungsi utama untuk meniru perilaku versi C ++" ""
    coba :
        nama file  =  sys . argv [ 1 ]
        graphfile  =  __load_binary ( nama file )
        partisi  =  partisi_baik ( graphfile )
        cetak  >>  sys . stderr , str ( modularity ( partisi , graphfile ))
        untuk  elem , part  in  partition . iteritems ():
            cetak  str ( elem ) +  ""  +  str ( bagian )
    kecuali ( IndexError , IOError ):
        print  "Usage: ./community filename"
        cetak  "temukan komunitas dalam nama file grafik dan tampilkan dendogram"
        cetak  "Parameter:"
        print  "nama file adalah file biner yang dihasilkan oleh"
        cetak  "utilitas konversi didistribusikan dengan implementasi C"

    

jika  __name__  ==  "__main__" :
    __main ()