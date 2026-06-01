"""Export predictions to ODS (Open Document Spreadsheet) format"""
import sqlite3
from datetime import datetime
from .config import get_db_path

def export_predictions_to_ods(filename=None):
    """
    Export all prophecy logs to ODS format
    Note: Requires ezodf or odfpy library
    """
    if filename is None:
        filename = f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ods"
    
    try:
        from odfpy import OpenDocumentSpreadsheet
        from odfpy import Table, TableRow, TableCell
        
        conn = sqlite3.connect(str(get_db_path()))
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT match_key, winner, confidence, home_rating, away_rating, prophecy, tier, created_at
            FROM prophecy_logs
            ORDER BY created_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        # Create ODS document
        doc = OpenDocumentSpreadsheet()
        
        # Note: Full ODS implementation would require odfpy package
        # For now, this is a placeholder
        print(f"[ ODS EXPORT PLACEHOLDER: Would save {len(rows)} predictions to {filename} ]")
        print("[ Install 'odfpy' to enable full ODS export: pip install odfpy ]")
        
    except ImportError:
        print("[ WARNING: odfpy not installed. Install with: pip install odfpy ]")

if __name__ == "__main__":
    export_predictions_to_ods()
