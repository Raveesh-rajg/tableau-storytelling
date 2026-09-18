import sys,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build_workbook import analyze, build, ROOT

def test_balanced_panel_and_weighted_denominator():
    data=analyze(); assert data['coverage']['countries']==142
    assert data['coverage']['observations']==1704
    assert data['trend'][0]['share_at_threshold']==pytest.approx(.011,abs=.001)
    assert data['trend'][-1]['share_at_threshold']==pytest.approx(.614,abs=.001)

def test_threshold_recomputes_monotonically():
    lower=analyze(60); upper=analyze(80)
    assert all(a['share_at_threshold']>=b['share_at_threshold'] for a,b in zip(lower['trend'],upper['trend']))

def test_country_gain_is_reproduced():
    data=analyze(); oman=next(r for r in data['changes'] if r['country']=='Oman')
    assert oman['gain_1952_2007']==pytest.approx(38.062)

def test_packaged_connections_are_relative_and_present():
    build()
    with zipfile.ZipFile(ROOT/'GlobalHealth.twbx') as z:
        xml=ET.fromstring(z.read('GlobalHealth.twb'))
        assert len(xml.findall('./worksheets/worksheet'))==4
        for conn in xml.findall('./datasources/datasource/connection'):
            assert conn.attrib['directory']+'/'+conn.attrib['filename'] in z.namelist()
