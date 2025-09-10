import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import {
  DataGrid,
  GridColDef,
  GridActionsCellItem,
  GridRowParams,
} from '@mui/x-data-grid';
import {
  Visibility as ViewIcon,
  Edit as EditIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';

interface Booking {
  id: number;
  booking_id: string;
  user_name: string;
  locker_number: string;
  item_type: string;
  status: string;
  created_at: string;
  pickup_time?: string;
  delivery_agent?: string;
  amount: number;
}

const Bookings: React.FC = () => {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [selectedBooking, setSelectedBooking] = useState<Booking | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    const mockBookings: Booking[] = [
      {
        id: 1,
        booking_id: 'BK-001',
        user_name: 'John Doe',
        locker_number: 'L-001',
        item_type: 'parcel',
        status: 'active',
        created_at: '2024-01-15 10:30',
        delivery_agent: 'Agent Smith',
        amount: 50,
      },
      {
        id: 2,
        booking_id: 'BK-002',
        user_name: 'Jane Smith',
        locker_number: 'L-005',
        item_type: 'food',
        status: 'completed',
        created_at: '2024-01-14 15:20',
        pickup_time: '2024-01-14 16:45',
        delivery_agent: 'Agent Johnson',
        amount: 75,
      },
    ];
    setBookings(mockBookings);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'warning';
      case 'completed': return 'success';
      case 'cancelled': return 'error';
      case 'pending': return 'info';
      default: return 'default';
    }
  };

  const columns: GridColDef[] = [
    { field: 'booking_id', headerName: 'Booking ID', width: 120 },
    { field: 'user_name', headerName: 'User', width: 150 },
    { field: 'locker_number', headerName: 'Locker', width: 100 },
    { field: 'item_type', headerName: 'Item Type', width: 120 },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.value}
          color={getStatusColor(params.value) as any}
          size="small"
        />
      ),
    },
    { field: 'delivery_agent', headerName: 'Agent', width: 150 },
    { field: 'created_at', headerName: 'Created', width: 150 },
    { field: 'pickup_time', headerName: 'Pickup Time', width: 150 },
    {
      field: 'amount',
      headerName: 'Amount',
      width: 100,
      renderCell: (params) => `₹${params.value}`,
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 150,
      getActions: (params: GridRowParams) => [
        <GridActionsCellItem
          icon={<ViewIcon />}
          label="View"
          onClick={() => {
            setSelectedBooking(params.row);
            setDialogOpen(true);
          }}
        />,
        <GridActionsCellItem
          icon={<EditIcon />}
          label="Edit"
          onClick={() => console.log('Edit', params.row.id)}
        />,
        <GridActionsCellItem
          icon={<CancelIcon />}
          label="Cancel"
          onClick={() => console.log('Cancel', params.row.id)}
          disabled={params.row.status === 'completed' || params.row.status === 'cancelled'}
        />,
      ],
    },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Booking Management
      </Typography>

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={bookings}
          columns={columns}
          pageSizeOptions={[10, 25, 50]}
          initialState={{
            pagination: {
              paginationModel: { page: 0, pageSize: 10 },
            },
          }}
          checkboxSelection
          disableRowSelectionOnClick
        />
      </Paper>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Booking Details - {selectedBooking?.booking_id}</DialogTitle>
        <DialogContent>
          {selectedBooking && (
            <Box sx={{ pt: 1 }}>
              <TextField
                fullWidth
                label="Booking ID"
                value={selectedBooking.booking_id}
                margin="normal"
                disabled
              />
              <TextField
                fullWidth
                label="User"
                value={selectedBooking.user_name}
                margin="normal"
                disabled
              />
              <TextField
                fullWidth
                label="Locker Number"
                value={selectedBooking.locker_number}
                margin="normal"
                disabled
              />
              <TextField
                fullWidth
                label="Item Type"
                value={selectedBooking.item_type}
                margin="normal"
                disabled
              />
              <TextField
                fullWidth
                label="Status"
                value={selectedBooking.status}
                margin="normal"
                disabled
              />
              <TextField
                fullWidth
                label="Delivery Agent"
                value={selectedBooking.delivery_agent || 'Not assigned'}
                margin="normal"
                disabled
              />
              <TextField
                fullWidth
                label="Amount"
                value={`₹${selectedBooking.amount}`}
                margin="normal"
                disabled
              />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Bookings;