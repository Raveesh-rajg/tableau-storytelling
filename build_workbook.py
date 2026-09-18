"""Reproduce the story's numerical evidence and author a portable Tableau workbook.

TWB source is inspectable; Tableau Desktop/Public rendering is a separate gate.
"""
from pathlib import Path
import csv,json,zipfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).parent

def analyze(threshold=70):
    with (ROOT/'data/gapminder.csv').open(encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    for row in rows:
        for k in ['year','pop']: row[k]=int(row[k])
        for k in ['lifeExp','gdpPercap']: row[k]=float(row[k])
    years=sorted({r['year'] for r in rows}); countries={r['country'] for r in rows}
    if len({(r['country'],r['year']) for r in rows})!=len(rows): raise ValueError('Duplicate country/year')
    trends=[]
    for year in years:
        group=[r for r in rows if r['year']==year]; pop=sum(r['pop'] for r in group)
        if len(group)!=len(countries): raise ValueError('Incomplete country panel')
        life=sorted(r['lifeExp'] for r in group); n=len(life)
        trends.append({'year':year,'median_life_expectancy':(life[(n-1)//2]+life[n//2])/2,
            'population':pop,'share_at_threshold':sum(r['pop'] for r in group if r['lifeExp']>=threshold)/pop})
    lookup={(r['country'],r['year']):r for r in rows}
    changes=[{'country':c,'gain_1952_2007':lookup[c,2007]['lifeExp']-lookup[c,1952]['lifeExp'],
        'change_1987_2007':lookup[c,2007]['lifeExp']-lookup[c,1987]['lifeExp']} for c in sorted(countries)]
    return {'rows':rows,'trend':trends,'changes':changes,'threshold':threshold,
            'coverage':{'countries':len(countries),'observations':len(rows),'years':years},
            'limitations':['National averages conceal within-country differences.','Population weighting covers only countries in this panel.','Income and health are associated; this dataset does not establish causality.']}

def csv_write(path,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def build():
    result=analyze(); out=ROOT/'outputs';out.mkdir(exist_ok=True)
    (out/'evidence.json').write_text(json.dumps(result,indent=2))
    charts=[('01 Population above 70 years','threshold_share.csv',[{'label':str(r['year']),'value':100*r['share_at_threshold']} for r in result['trend']],'Percent of panel population','Line'),
      ('02 Median life expectancy','median_life.csv',[{'label':str(r['year']),'value':r['median_life_expectancy']} for r in result['trend']],'Years','Line'),
      ('03 Largest gains 1952 to 2007','largest_gains.csv',[{'label':r['country'],'value':r['gain_1952_2007']} for r in sorted(result['changes'],key=lambda r:r['gain_1952_2007'],reverse=True)[:10]],'Gain in years','Bar'),
      ('04 Largest declines 1987 to 2007','largest_declines.csv',[{'label':r['country'],'value':r['change_1987_2007']} for r in sorted(result['changes'],key=lambda r:r['change_1987_2007'])[:10]],'Change in years','Bar')]
    workbook=ET.Element('workbook',{'source-platform':'win','version':'18.1','xmlns:user':'http://www.tableausoftware.com/xml/user'})
    ET.SubElement(workbook,'preferences');sources=ET.SubElement(workbook,'datasources');sheets=ET.SubElement(workbook,'worksheets');windows=ET.SubElement(workbook,'windows')
    for i,(title,file,rows,unit,mark) in enumerate(charts):
        csv_write(out/file,rows);name=f'story{i}'
        source=ET.SubElement(sources,'datasource',{'caption':title,'inline':'true','name':name,'version':'18.1'})
        conn=ET.SubElement(source,'connection',{'class':'textscan','directory':'outputs','filename':file,'separator':',','header':'yes'})
        ET.SubElement(conn,'relation',{'name':file,'table':f'[{file}]','type':'table'})
        columns=[{'caption':'Year' if mark=='Line' else 'Country','datatype':'string','name':'[label]','role':'dimension','type':'nominal'},
                 {'caption':unit,'datatype':'real','name':'[value]','role':'measure','type':'quantitative'}]
        for attrs in columns: ET.SubElement(source,'column',attrs)
        sheet=ET.SubElement(sheets,'worksheet',{'name':title});layout=ET.SubElement(sheet,'layout-options');ET.SubElement(layout,'title')
        table=ET.SubElement(sheet,'table');view=ET.SubElement(table,'view');ds=ET.SubElement(view,'datasources');ET.SubElement(ds,'datasource',{'caption':title,'name':name})
        dep=ET.SubElement(view,'datasource-dependencies',{'datasource':name})
        for attrs in columns: ET.SubElement(dep,'column',attrs)
        ET.SubElement(dep,'column-instance',{'column':'[label]','derivation':'None','name':'[none:label:nk]','pivot':'key','type':'nominal'})
        ET.SubElement(dep,'column-instance',{'column':'[value]','derivation':'Sum','name':'[sum:value:qk]','pivot':'key','type':'quantitative'})
        ET.SubElement(view,'aggregation',{'value':'true'});ET.SubElement(table,'style')
        pane=ET.SubElement(ET.SubElement(table,'panes'),'pane',{'selection-relaxation-option':'selection-relaxation-allow'})
        ET.SubElement(pane,'view',{'breakdown':'auto'});ET.SubElement(pane,'mark',{'class':mark})
        ET.SubElement(table,'rows').text=f'[{name}].[sum:value:qk]' if mark=='Line' else f'[{name}].[none:label:nk]'
        ET.SubElement(table,'cols').text=f'[{name}].[none:label:nk]' if mark=='Line' else f'[{name}].[sum:value:qk]'
        ET.SubElement(windows,'window',{'class':'worksheet','name':title})
    ET.indent(workbook)
    twb=ROOT/'GlobalHealth.twb';ET.ElementTree(workbook).write(twb,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(ROOT/'GlobalHealth.twbx','w',zipfile.ZIP_DEFLATED) as z:
        z.write(twb,twb.name)
        for _,file,*_ in charts: z.write(out/file,f'outputs/{file}')
    print(json.dumps({'coverage':result['coverage'],'first':result['trend'][0],'last':result['trend'][-1]},indent=2))

if __name__=='__main__': build()
