import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { Visibility, Cancel, CheckCircle } from '@mui/icons-material';

interface Booking {
  id: number;
  bookingId: string;
  customerName: string;
  customerPhone: string;
  lockerName: string;
  itemType: string;
  status: 'pending' | 'active' | 'completed' | 'cancelled';
  createdAt: string;
  expiresAt: string;
  amount: number;
}

const SimpleBookings: React.FC = () => {
  const [bookings] = useState<Booking[]>([
    {
      id: 1,
      bookingId: 'BK001',
      customerName: 'John Doe',
      customerPhone: '+91 9876543210',
      lockerName: 'L-001',
      itemType: 'Package',
      status: 'active',
      createdAt: '2024-01-16 09:30',
      expiresAt: '2024-01-18 09:30',
      amount: 50,
    },
    {
      id: 2,
      bookingId: 'BK002',
      customerName: 'Jane Smith',
      customerPhone: '+91 9876543211',
      lockerName: 'L-006',
      itemType: 'Food',
      status: 'pending',
      createdAt: '2024-01-16 10:15',
      expiresAt: '2024-01-16 14:15',
      amount: 30,
    },
    {
      id: 3,
      bookingId: 'BK003',
      customerName: 'Mike Johnson',
      customerPhone: '+91 9876543212',
      lockerName: 'L-003',
      itemType: 'Documents',
      status: 'completed',
      createdAt: '2024-01-15 14:20',
      expiresAt: '2024-01-16 14:20',
      amount: 25,
    },
    {
      id: 4,
      bookingId: 'BK004',
      customerName: 'Sarah Wilson',
      customerPhone: '+91 9876543213',
      lockerName: 'L-002',
      itemType: 'Laundry',
      status: 'cancelled',
      createdAt: '2024-01-14 11:45',
      expiresAt: '2024-01-15 11:45',
      amount: 40,
    },
  ]);

  const [filterStatus, setFilterStatus] = useState('all');

  const filteredBookings = bookings.filter((booking) => {
    return filterStatus === 'all' || booking.status === filterStatus;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'warning';
      case 'active': return 'info';
      case 'completed': return 'success';
      case 'cancelled': return 'error';
      default: return 'default';
    }
  };

  const getItemTypeColor = (itemType: string) => {
    switch (itemType) {
      case 'Package': return 'primary';
      case 'Food': return 'secondary';
      case 'Documents': return 'info';
      case 'Laundry': return 'success';
      default: return 'default';
    }
  };

  const handleBookingAction = (booking: Booking, action: string) => {
    console.log(`${action} booking ${booking.bookingId}`);
    // Here you would typically make an API call
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
        <Typography variant="h4">Bookings Management</Typography>
        
        <FormControl sx={{ minWidth: 150 }}>
          <InputLabel>Filter Status</InputLabel>
          <Select
            value={filterStatus}
            label="Filter Status"
            onChange={(e) => setFilterStatus(e.target.value)}
          >
            <MenuItem value="all">All Status</MenuItem>
            <MenuItem value="pending">Pending</MenuItem>
            <MenuItem value="active">Active</MenuItem>
            <MenuItem value="completed">Completed</MenuItem>
            <MenuItem value="cancelled">Cancelled</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Booking ID</TableCell>
                <TableCell>Customer</TableCell>
                <TableCell>Phone</TableCell>
                <TableCell>Locker</TableCell>
                <TableCell>Item Type</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Created</TableCell>
                <TableCell>Expires</TableCell>
                <TableCell>Amount</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredBookings.map((booking) => (
                <TableRow key={booking.id}>
                  <TableCell>
                    <Typography variant="body2" fontWeight="bold">
                      {booking.bookingId}
                    </Typography>
                  </TableCell>
                  <TableCell>{booking.customerName}</TableCell>
                  <TableCell>{booking.customerPhone}</TableCell>
                  <TableCell>
                    <Chip label={booking.lockerName} size="small" />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={booking.itemType}
                      color={getItemTypeColor(booking.itemType) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={booking.status}
                      color={getStatusColor(booking.status) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {booking.createdAt}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {booking.expiresAt}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" fontWeight="bold">
                      ₹{booking.amount}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Box display="flex" gap={1}>
                      <Button
                        size="small"
                        startIcon={<Visibility />}
                        onClick={() => handleBookingAction(booking, 'view')}
                      >
                        View
                      </Button>
                      {booking.status === 'pending' && (
                        <Button
                          size="small"
                          color="success"
                          startIcon={<CheckCircle />}
                          onClick={() => handleBookingAction(booking, 'approve')}
                        >
                          Approve
                        </Button>
                      )}
                      {(booking.status === 'pending' || booking.status === 'active') && (
                        <Button
                          size="small"
                          color="error"
                          startIcon={<Cancel />}
                          onClick={() => handleBookingAction(booking, 'cancel')}
                        >
                          Cancel
                        </Button>
                      )}
                    </Box>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {filteredBookings.length === 0 && (
        <Box textAlign="center" sx={{ mt: 4 }}>
          <Typography variant="h6" color="textSecondary">
            No bookings found matching the selected filter.
          </Typography>
        </Box>
      )}

      {/* Summary Cards */}
      <Box display="flex" flexWrap="wrap" gap={2} sx={{ mt: 3 }}>
        <Paper sx={{ p: 2, minWidth: 200 }}>
          <Typography variant="h6" color="warning.main">
            Pending: {bookings.filter(b => b.status === 'pending').length}
          </Typography>
        </Paper>
        <Paper sx={{ p: 2, minWidth: 200 }}>
          <Typography variant="h6" color="info.main">
            Active: {bookings.filter(b => b.status === 'active').length}
          </Typography>
        </Paper>
        <Paper sx={{ p: 2, minWidth: 200 }}>
          <Typography variant="h6" color="success.main">
            Completed: {bookings.filter(b => b.status === 'completed').length}
          </Typography>
        </Paper>
        <Paper sx={{ p: 2, minWidth: 200 }}>
          <Typography variant="h6" color="error.main">
            Cancelled: {bookings.filter(b => b.status === 'cancelled').length}
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
};

export default SimpleBookings;