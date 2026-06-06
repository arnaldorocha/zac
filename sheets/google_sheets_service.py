"""
Google Sheets integration service.
Provides free integration with Google Sheets using pygsheets (no paid APIs).
"""
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """Handles Google Sheets operations without paid APIs."""
    
    def __init__(self, credentials_path: str = "credentials.json"):
        """
        Initialize Google Sheets service.
        
        Args:
            credentials_path: Path to credentials JSON file
        """
        self.credentials_path = credentials_path
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize Google Sheets client."""
        try:
            import pygsheets
            
            # Try to authorize with credentials file
            if Path(self.credentials_path).exists():
                self.client = pygsheets.authorize(
                    service_account_file=self.credentials_path
                )
                logger.info("Connected to Google Sheets API")
            else:
                logger.warning(f"Credentials file not found at {self.credentials_path}")
                logger.info("To set up Google Sheets integration:")
                logger.info("1. Go to https://console.cloud.google.com")
                logger.info("2. Create a service account")
                logger.info("3. Download credentials.json")
                logger.info("4. Place it in the project root")
        except ImportError:
            logger.error("pygsheets not installed. Install with: pip install pygsheets")
            self.client = None
        except Exception as e:
            logger.error(f"Error initializing Google Sheets client: {e}")
            self.client = None
    
    def open_spreadsheet(self, spreadsheet_title: str) -> Optional[Any]:
        """Open a spreadsheet by title."""
        if not self.client:
            logger.error("Google Sheets client not initialized")
            return None
        
        try:
            spreadsheet = self.client.open(spreadsheet_title)
            logger.info(f"Opened spreadsheet: {spreadsheet_title}")
            return spreadsheet
        except Exception as e:
            logger.error(f"Error opening spreadsheet {spreadsheet_title}: {e}")
            return None
    
    def open_spreadsheet_by_key(self, spreadsheet_key: str) -> Optional[Any]:
        """Open a spreadsheet by key."""
        if not self.client:
            logger.error("Google Sheets client not initialized")
            return None
        
        try:
            spreadsheet = self.client.open_by_key(spreadsheet_key)
            logger.info(f"Opened spreadsheet by key: {spreadsheet_key}")
            return spreadsheet
        except Exception as e:
            logger.error(f"Error opening spreadsheet by key: {e}")
            return None
    
    def append_row(
        self,
        spreadsheet: Any,
        sheet_title: str,
        values: List[Any]
    ) -> bool:
        """Append a row to worksheet."""
        if not spreadsheet:
            logger.error("Spreadsheet not provided")
            return False
        
        try:
            worksheet = spreadsheet.worksheet_by_title(sheet_title)
            worksheet.append_table(values, dimension='ROWS')
            logger.info(f"Row appended to {sheet_title}")
            return True
        except Exception as e:
            logger.error(f"Error appending row: {e}")
            return False
    
    def update_cell(
        self,
        spreadsheet: Any,
        sheet_title: str,
        row: int,
        col: int,
        value: Any
    ) -> bool:
        """Update a single cell."""
        if not spreadsheet:
            logger.error("Spreadsheet not provided")
            return False
        
        try:
            worksheet = spreadsheet.worksheet_by_title(sheet_title)
            worksheet.update_value((row, col), value)
            logger.info(f"Cell ({row}, {col}) updated to {value}")
            return True
        except Exception as e:
            logger.error(f"Error updating cell: {e}")
            return False
    
    def get_cell(
        self,
        spreadsheet: Any,
        sheet_title: str,
        row: int,
        col: int
    ) -> Optional[Any]:
        """Get value from cell."""
        if not spreadsheet:
            logger.error("Spreadsheet not provided")
            return None
        
        try:
            worksheet = spreadsheet.worksheet_by_title(sheet_title)
            cell = worksheet.cell((row, col))
            return cell.value
        except Exception as e:
            logger.error(f"Error getting cell: {e}")
            return None
    
    def get_all_values(
        self,
        spreadsheet: Any,
        sheet_title: str
    ) -> Optional[List[List[Any]]]:
        """Get all values from worksheet."""
        if not spreadsheet:
            logger.error("Spreadsheet not provided")
            return None
        
        try:
            worksheet = spreadsheet.worksheet_by_title(sheet_title)
            all_values = worksheet.get_all_values()
            logger.info(f"Retrieved {len(all_values)} rows from {sheet_title}")
            return all_values
        except Exception as e:
            logger.error(f"Error getting all values: {e}")
            return None
    
    def find_row(
        self,
        spreadsheet: Any,
        sheet_title: str,
        search_value: str,
        column: int = 1
    ) -> Optional[int]:
        """Find row containing value."""
        if not spreadsheet:
            logger.error("Spreadsheet not provided")
            return None
        
        try:
            worksheet = spreadsheet.worksheet_by_title(sheet_title)
            all_values = worksheet.get_all_values()
            
            for idx, row in enumerate(all_values, 1):
                if len(row) >= column and row[column - 1] == search_value:
                    return idx
            
            return None
        except Exception as e:
            logger.error(f"Error finding row: {e}")
            return None
    
    def create_worksheet(
        self,
        spreadsheet: Any,
        title: str,
        rows: int = 100,
        cols: int = 10
    ) -> Optional[Any]:
        """Create new worksheet."""
        if not spreadsheet:
            logger.error("Spreadsheet not provided")
            return None
        
        try:
            worksheet = spreadsheet.add_worksheet(title, rows=rows, cols=cols)
            logger.info(f"Created worksheet: {title}")
            return worksheet
        except Exception as e:
            logger.error(f"Error creating worksheet: {e}")
            return None
    
    def log_expense(
        self,
        spreadsheet: Any,
        date: str,
        category: str,
        description: str,
        amount: float
    ) -> bool:
        """Log expense to spreadsheet."""
        try:
            row_data = [date, category, description, str(amount)]
            return self.append_row(spreadsheet, "Gastos", row_data)
        except Exception as e:
            logger.error(f"Error logging expense: {e}")
            return False
    
    def log_study(
        self,
        spreadsheet: Any,
        date: str,
        discipline: str,
        hours: float
    ) -> bool:
        """Log study session to spreadsheet."""
        try:
            row_data = [date, discipline, str(hours)]
            return self.append_row(spreadsheet, "Estudos", row_data)
        except Exception as e:
            logger.error(f"Error logging study: {e}")
            return False
    
    def log_goal(
        self,
        spreadsheet: Any,
        date: str,
        goal: str,
        status: str
    ) -> bool:
        """Log goal to spreadsheet."""
        try:
            row_data = [date, goal, status]
            return self.append_row(spreadsheet, "Metas", row_data)
        except Exception as e:
            logger.error(f"Error logging goal: {e}")
            return False
