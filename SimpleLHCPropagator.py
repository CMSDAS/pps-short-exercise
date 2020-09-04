import ROOT
import numpy as np

class SimpleLHCPropagator:
    def __init__( self, files, verbose=False ):
        
        if not isinstance( files, dict ):
            raise RuntimeError( "Provide file paths indexed by crossing angle value: { XANGLE : PATH }." )
            
        self.files_ = files
        self.verbose_ = verbose
        
        self.open_root_files_ = {}
        
        RPInfo_ = {}
        RPInfo_[0x76180000] = { "dirName" : "XRPH_D6L5_B2", "zPos" : -21255.1 }
        RPInfo_[0x7a700000] = { "dirName" : "XRPH_E6L5_B2", "zPos" : -21570.0 }
        RPInfo_[0x78980000] = { "dirName" : "XRPH_B6L5_B2", "zPos" : -21955.0 }
        RPInfo_[0x77180000] = { "dirName" : "XRPH_D6R5_B1", "zPos" : +21255.1 }
        RPInfo_[0x7b700000] = { "dirName" : "XRPH_E6R5_B1", "zPos" : +21570.0 }
        RPInfo_[0x79980000] = { "dirName" : "XRPH_B6R5_B1", "zPos" : +21955.0 }

        self.RPInfoId_ = {}
        for key in RPInfo_:
            arm, station, rp = self.rp_index( key )
            rpid = 100*arm + 10*station + rp
            self.RPInfoId_[rpid] = RPInfo_[key]
            
        self.OF_tags_ = ( "v_x",
                          "L_x",
                          "E_14",
                          "x_D",
                          "vp_x",
                          "Lp_x",
                          "E_24",
                          "xp_D",
                          "E_32",
                          "v_y",
                          "L_y",
                          "y_D",
                          "E_42",
                          "vp_y",
                          "Lp_y",
                          "yp_D"
                         )
        self.OF_tags_main_ = ( "x_D", "v_x", "L_x", "y_D", "v_y", "L_y" )

        self.draw_xtitles_ = {}
        self.draw_xtitles_[ "x_D" ] = "#xi"
        self.draw_xtitles_[ "xi_vs_x" ] = "x (cm)"
        self.draw_xtitles_[ "v_x" ] = "#xi"
        self.draw_xtitles_[ "L_x" ] = "#xi"
        self.draw_xtitles_[ "y_D" ] = "#xi"
        self.draw_xtitles_[ "v_y" ] = "#xi"
        self.draw_xtitles_[ "L_y" ] = "#xi"
        self.draw_ytitles_ = {}
        self.draw_ytitles_[ "x_D" ] = "x_{D} (cm)"
        self.draw_ytitles_[ "xi_vs_x" ] = "#xi(x)"
        self.draw_ytitles_[ "v_x" ] = "v_{x}"
        self.draw_ytitles_[ "L_x" ] = "L_{x} (cm)"
        self.draw_ytitles_[ "y_D" ] = "y_{D} (cm)"
        self.draw_ytitles_[ "v_y" ] = "v_{y}"
        self.draw_ytitles_[ "L_y" ] = "L_{y} (cm)"

        # Map of files per crossing angle
        self.principal_xangles_ = None
        self.optical_functions_ = {}
        if isinstance(self.files_, dict):
            self.principal_xangles_ = list( self.files_.keys() )
            for xangle in self.principal_xangles_:
                print ( "Accessing optical functions for crossing angle {}".format( xangle ) )
                self.optical_functions_[ xangle ] = {}
                path_ = self.files_[ xangle ]
                for rpid in self.RPInfoId_:
                    self.optical_functions_[ xangle ][ rpid ] = {}
                    for tag in self.OF_tags_main_:
                        gr_ = self.get_function( xangle, rpid, tag )
                        # x is xi 
                        x_ = gr_.GetX()
                        y_ = gr_.GetY()
                        spl_ = ROOT.TSpline3( "{}_{}_{}".format( str(xangle), str(rpid), tag ), x_, y_, len( x_) )
                        self.optical_functions_[ xangle ][ rpid ][ tag ] = spl_

                        if tag == "x_D":
                            inv_tag_ = "xi_vs_x"
                            inv_x_ = y_
                            inv_y_ = x_
                            self.optical_functions_[ xangle ][ rpid ][ inv_tag_ ] = ROOT.TSpline3( "{}_{}_{}".format( str(xangle), str(rpid), inv_tag_ ), inv_x_, inv_y_, len( inv_x_) )
                            
        print ( self.optical_functions_ )
        print ( self.open_root_files_ )
        for file_ in self.open_root_files_:
            self.open_root_files_[ file_ ].Close()

    def set_verbose( self, flag ):
        self.verbose_ = flag
    
    def rp_index( self, key ):
        index_ = ( ( ( (key & ~0xFFFFFF) >> 24 ) & 0x1 ), ( ( (key & ~0x3FFFFF) >> 22 ) & 0x3 ), ( ( (key & ~0x7FFFF)  >> 19 ) & 0x7 ) )
        return index_
    
    def get_function( self, xangle, rpid, tag ):
        path_ = self.RPInfoId_[rpid]["dirName"] + "/g_" + tag + "_vs_xi";
        print ( "Accessing {}".format( path_ ) )
        file_ = self.files_[ xangle ]
        rootFile_ = ROOT.TFile( file_ , "READ" )
        if not file_ in self.open_root_files_:
            self.open_root_files_[ file_ ] = rootFile_
        obj_ = rootFile_.Get( path_ )
        return obj_
    
    def of_tags( self):
        return self.OF_tags_main_
    
    def draw_function( self, xangle, rpid, tag):
        w = 800
        h = 600
        canvas_ = ROOT.TCanvas( "canvas_{}_{}_{}".format( xangle, rpid, tag ), "", w, h )
        canvas_.SetLeftMargin( 0.15 )
        function_ = self.optical_functions_[ xangle ][ rpid ][ tag ]
        xmin_ = function_.GetXmin()
        xmax_ = function_.GetXmax()
        y1_ = function_.Eval( xmin_ ) 
        y2_ = function_.Eval( xmax_ ) 
        frame_ = canvas_.DrawFrame( xmin_, np.min( (y1_,y2_) ), xmax_, np.max( (y1_,y2_) ) )
        frame_.GetXaxis().SetTitle( self.draw_xtitles_[ tag ] )
        frame_.GetYaxis().SetTitle( self.draw_ytitles_[ tag ] )
        function_.Draw( "SAME" )
        canvas_.Draw()
        return ( function_, canvas_ )
    
    def draw_function_vs_rpid( self, xangle, tag):
        w = 800
        h = 600
        canvas_ = ROOT.TCanvas( "canvas_{}_{}".format( xangle, tag ), "", w, h )
        canvas_.SetLeftMargin( 0.15 )
        functions_ = []
        for rpid in self.RPInfoId_:
            functions_.append( self.optical_functions_[ xangle ][ rpid ][ tag ] )
            if len( functions_ ) == 1:
                xmin_ = functions_[-1].GetXmin()
                xmax_ = functions_[-1].GetXmax()
                y1_ = functions_[-1].Eval( xmin_ ) 
                y2_ = functions_[-1].Eval( xmax_ ) 
                frame_ = canvas_.DrawFrame( xmin_, np.min( (y1_,y2_) ), xmax_, np.max( (y1_,y2_) ) )
                frame_.GetXaxis().SetTitle( self.draw_xtitles_[ tag ] )
                frame_.GetYaxis().SetTitle( self.draw_ytitles_[ tag ] )

            functions_[-1].Draw("SAME")
            
        canvas_.Draw()
        return ( functions_, canvas_ )

    def draw_function_vs_xangle( self, rpid, tag):
        w = 800
        h = 600
        canvas_ = ROOT.TCanvas( "canvas_{}_{}".format( rpid, tag ), "", w, h )
        canvas_.SetLeftMargin( 0.15 )
        functions_ = []
        for xangle in self.principal_xangles_:
            functions_.append( self.optical_functions_[ xangle ][ rpid ][ tag ] )
            if len( functions_ ) == 1:
                xmin_ = functions_[-1].GetXmin()
                xmax_ = functions_[-1].GetXmax()
                y1_ = functions_[-1].Eval( xmin_ ) 
                y2_ = functions_[-1].Eval( xmax_ ) 
                frame_ = canvas_.DrawFrame( xmin_, np.min( (y1_,y2_) ), xmax_, np.max( (y1_,y2_) ) )
                frame_.GetXaxis().SetTitle( self.draw_xtitles_[ tag ] )
                frame_.GetYaxis().SetTitle( self.draw_ytitles_[ tag ] )

            functions_[-1].Draw("SAME")
            
        canvas_.Draw()
        return ( functions_, canvas_ )

    def eval( self, rpid, xangle, tag, x ):

        interpolate_ = True
        if xangle in self.principal_xangles_:
            interpolate_ = False

        #tags_to_interpolate_ = [ "x_D" ]
        tags_to_interpolate_ = [ "x_D", "xi_vs_x" ]

        xangle1_ = None
        xangle2_ = None
        if interpolate_:
            arr_ = np.array( self.principal_xangles_ )
            if xangle < arr_[0]:
                xangle1_ = arr_[0]
                xangle2_ = arr_[1]
            elif xangle > arr_[-1]:
                xangle1_ = arr_[-2]
                xangle2_ = arr_[-1]
            else:
                xangle1_ = arr_[ arr_ <= xangle ][-1]
                xangle2_ = arr_[ arr_ >= xangle ][0]

        if self.verbose_: print ( "Principal crossing angle values:", self.principal_xangles_ )        
        if self.verbose_: print ( "Interpolate: {}".format( interpolate_ ) )   

        val_ = None
        if interpolate_ and tag in tags_to_interpolate_: 
            function1_ = self.optical_functions_[ xangle1_ ][ rpid ][ tag ]
            function2_ = self.optical_functions_[ xangle2_ ][ rpid ][ tag ]
            val_ = function1_.Eval( x ) + ( function2_.Eval( x ) - function1_.Eval( x ) ) * ( xangle - xangle1_ ) / ( xangle2_ - xangle1_ )
        else:
            xangle_ref_ = None
            if tag in tags_to_interpolate_:
                xangle_ref_ = xangle
            else:
                xangle_ref_ = self.principal_xangles_[0]

            function_ = self.optical_functions_[ xangle_ref_ ][ rpid ][ tag ]
            val_ = function_.Eval( x )

        return val_

    def transport( self, rpid, xangle, kinematics ):
        
        x = kinematics[0]
        theta_x = kinematics[1]
        y = kinematics[2]
        theta_y = kinematics[3]
        xi = kinematics[4]
        
        interpolate_ = True
        if xangle in self.principal_xangles_:
            interpolate_ = False

        tags_to_interpolate_ = [ "x_D" ]

        xangle1_ = None
        xangle2_ = None
        if interpolate_:
            arr_ = np.array( self.principal_xangles_ )
            if xangle < arr_[0]:
                xangle1_ = arr_[0]
                xangle2_ = arr_[1]
            elif xangle > arr_[-1]:
                xangle1_ = arr_[-2]
                xangle2_ = arr_[-1]
            else:
                xangle1_ = arr_[ arr_ <= xangle ][-1]
                xangle2_ = arr_[ arr_ >= xangle ][0]

        if self.verbose_: print ( "Principal crossing angle values:", self.principal_xangles_ )        
        if self.verbose_: print ( "Interpolate: {}".format( interpolate_ ) )   
        
        values_ = {}
        for tag in self.OF_tags_main_:
            if interpolate_ and tag in tags_to_interpolate_: 
                function1_ = self.optical_functions_[ xangle1_ ][ rpid ][ tag ]
                function2_ = self.optical_functions_[ xangle2_ ][ rpid ][ tag ]
                val_ = function1_.Eval( xi ) + ( function2_.Eval( xi ) - function1_.Eval( xi ) ) * ( xangle - xangle1_ ) / ( xangle2_ - xangle1_ )
                values_[ tag ] = val_
            else:
                xangle_ref_ = None
                if tag in tags_to_interpolate_:
                    xangle_ref_ = xangle
                else:
                    xangle_ref_ = self.principal_xangles_[0]

                function_ = self.optical_functions_[ xangle_ref_ ][ rpid ][ tag ]
                val_ = function_.Eval( xi )
                values_[ tag ] = val_
               
        if self.verbose_: print ( values_ )
        
        x_ = values_[ 'x_D' ] + values_[ 'v_x' ] * x + values_[ 'L_x' ] * theta_x
        y_ = values_[ 'y_D' ] + values_[ 'v_y' ] * y + values_[ 'L_y' ] * theta_y
        z_ = self.RPInfoId_[ rpid ][ "zPos" ]
        
        if self.verbose_: print ( "Transverse position in detector: ({},{})".format( x_, y_ ) )
        if self.verbose_: print ( "RP position: {}".format( z_ ) )
        
        return ( x_, y_, z_ )
