// Generate HTML for cards UI from json supplied from python backend

function generate_cards(json_data, companies_list) {
    json_obj = JSON.parse(json_data)
    var new_output_html = `<div class = "row" style="padding:10px">
        <div class="col-sm-6">      
            <h1 style="text-align : center">Nifty 50 stocks</h1>
        <div class="col-sm-6">        
          <div class="card card-block" style="background-color : #f1f1f1; border-color : #f1f1f1; text-align : center;">
            <h4 class="card-title" style="text-align:center;">ACC</h4>                
                <h3>1451.35</h3>
          </div>        
        </div>  
        <div class="col-sm-6">
          <div class="card card-block" style="background-color : #f1f1f1; border-color : #f1f1f1; text-align : center;">
            <h4 class="card-title" style="text-align:center;">ADANIPORTS</h4>                
                <table width = 50% align="center">
                    <tr align = "center">
                        <td><h3>202.35</h3></td>
                        <td><font color="green"><i class="fa fa-chevron-up"
                                                   style="{text-color:green}"aria-hidden="true">
                                                </i>&nbsp;2.25</font></td>
                    </tr>
              </table>
          </div>        
        </div> 
        </div>
        </div>`
    var counter = 0;
    var output_html = '';
    scrips = json_obj.scrips
    for (scrip of scrips) {
        if (counter % 2 == 0) {
            output_html += '<div class = "row" style="padding:10px"><div class = "col-sm-6">\r';
        }
        output_html += `<div class = "col-sm-6">
                            <div class="card card-block" style="background-color : #f1f1f1; border-color : #f1f1f1; text-align : center;">\n`;
        output_html += '<h4 class="card-title" style="text-align:center;">';
        output_html += scrip
        output_html += `</h4>\n
                            <table width = 50% align="center">
                              <tr align = "center">
                                    <td><h3>`+json_obj[scrip].ltp+`</h3>
                                    </td>\n`;
        if (json_obj[scrip].chg.startsWith('+')){
            output_html += `\t\t\t\t\t\t\t\t<td>
                                  <font color="green">
                                    <i class="fa fa-chevron-up" style="{text-color:green}"aria-hidden="true">
                                    </i>&nbsp;`+json_obj[scrip].chg+`(`+json_obj[scrip].pc_chg+`%)
                                  </font>
                                </td>\n\t\t\t`
        }
        else {
            output_html += '<td>\r<font color="red">\r<i class="fa fa-chevron-down" style="{text-color:red}"aria-hidden="true"></i>&nbsp;'+json_obj[scrip].chg+' ('+json_obj[scrip].pc_chg+'%) </font>\r</td>\r'
        }
        output_html += `\t\t\t\t</tr>\r
                        </table>\n`
        output_html+= `\t\t\t\t</div>\r
            </div>\n`;
        if (counter %2 != 0) {
            output_html += `    </div>\r
                        </div>\n`;
        }
        counter +=1;
    }
    //alert(output_html);
    return output_html;
}
