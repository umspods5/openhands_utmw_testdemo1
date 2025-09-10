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
import { Visibility, Receipt, Refresh } from '@mui/icons-material';

interface Payment {
  id: number;
  transactionId: string;
  bookingId: string;
  customerName: string;
  amount: number;
  status: 'pending' | 'completed' | 'failed' | 'refunded';
  paymentMethod: string;
  createdAt: string;
  completedAt?: string;
}

const SimplePayments: React.FC = () => {
  const [payments] = useState<Payment[]>([
    {
      id: 1,
      transactionId: 'TXN001',
      bookingId: 'BK001',
      customerName: 'John Doe',
      amount: 50,
      status: 'completed',
      paymentMethod: 'UPI',
      createdAt: '2024-01-16 09:30',
      completedAt: '2024-01-16 09:31',
    },
    {
      id: 2,
      transactionId: 'TXN002',
      bookingId: 'BK002',
      customerName: 'Jane Smith',
      amount: 30,
      status: 'pending',
      paymentMethod: 'Credit Card',
      createdAt: '2024-01-16 10:15',
    },
    {
      id: 3,
      transactionId: 'TXN003',
      bookingId: 'BK003',
      customerName: 'Mike Johnson',
      amount: 25,
      status: 'completed',
      paymentMethod: 'Debit Card',
      createdAt: '2024-01-15 14:20',
      completedAt: '2024-01-15 14:21',
    },
    {
      id: 4,
      transactionId: 'TXN004',
      bookingId: 'BK004',
      customerName: 'Sarah Wilson',
      amount: 40,
      status: 'refunded',
      paymentMethod: 'UPI',
      createdAt: '2024-01-14 11:45',
      completedAt: '2024-01-14 12:30',
    },
    {
      id: 5,
      transactionId: 'TXN005',
      bookingId: 'BK005',
      customerName: 'David Brown',
      amount: 75,
      status: 'failed',
      paymentMethod: 'Net Banking',
      createdAt: '2024-01-13 16:20',
    },
  ]);

  const [filterStatus, setFilterStatus] = useState('all');

  const filteredPayments = payments.filter((payment) => {
    return filterStatus === 'all' || payment.status === filterStatus;
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'warning';
      case 'completed': return 'success';
      case 'failed': return 'error';
      case 'refunded': return 'info';
      default: return 'default';
    }
  };

  const getPaymentMethodColor = (method: string) => {
    switch (method) {
      case 'UPI': return 'primary';
      case 'Credit Card': return 'secondary';
      case 'Debit Card': return 'info';
      case 'Net Banking': return 'success';
      default: return 'default';
    }
  };

  const handlePaymentAction = (payment: Payment, action: string) => {
    console.log(`${action} payment ${payment.transactionId}`);
    // Here you would typically make an API call
  };

  const getTotalAmount = (status?: string) => {
    const filtered = status ? payments.filter(p => p.status === status) : payments;
    return filtered.reduce((sum, payment) => sum + payment.amount, 0);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
        <Typography variant="h4">Payments Management</Typography>
        
        <FormControl sx={{ minWidth: 150 }}>
          <InputLabel>Filter Status</InputLabel>
          <Select
            value={filterStatus}
            label="Filter Status"
            onChange={(e) => setFilterStatus(e.target.value)}
          >
            <MenuItem value="all">All Status</MenuItem>
            <MenuItem value="pending">Pending</MenuItem>
            <MenuItem value="completed">Completed</MenuItem>
            <MenuItem value="failed">Failed</MenuItem>
            <MenuItem value="refunded">Refunded</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Summary Cards */}
      <Box display="flex" flexWrap="wrap" gap={2} sx={{ mb: 3 }}>
        <Paper sx={{ p: 2, minWidth: 200 }}>
          <Typography variant="h6" color="success.main">
            Total Revenue
          </Typography>
          <Typography variant="h4">
            ₹{getTotalAmount('completed').toLocaleString()}
          </Typography>
        </Paper>
        <Paper sx={{ p: 2, minWidth: 200 }}>
          <Typography variant="h6" color="warning.main">
            Pending
          </Typography>
          <Typography variant="h4">
            ₹{getTotalAmount('pending').toLocaleString()}
          </Typography>
        </Paper>
        <Paper sx={{ p: 2, minWidth: 200 }}>
          <Typography variant="h6" color="error.main">
            Failed
          </Typography>
          <Typography variant="h4">
            ₹{getTotalAmount('failed').toLocaleString()}
          </Typography>
        </Paper>
        <Paper sx={{ p: 2, minWidth: 200 }}>
          <Typography variant="h6" color="info.main">
            Refunded
          </Typography>
          <Typography variant="h4">
            ₹{getTotalAmount('refunded').toLocaleString()}
          </Typography>
        </Paper>
      </Box>

      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Transaction ID</TableCell>
                <TableCell>Booking ID</TableCell>
                <TableCell>Customer</TableCell>
                <TableCell>Amount</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Payment Method</TableCell>
                <TableCell>Created</TableCell>
                <TableCell>Completed</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredPayments.map((payment) => (
                <TableRow key={payment.id}>
                  <TableCell>
                    <Typography variant="body2" fontWeight="bold">
                      {payment.transactionId}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip label={payment.bookingId} size="small" />
                  </TableCell>
                  <TableCell>{payment.customerName}</TableCell>
                  <TableCell>
                    <Typography variant="body2" fontWeight="bold">
                      ₹{payment.amount}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={payment.status}
                      color={getStatusColor(payment.status) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={payment.paymentMethod}
                      color={getPaymentMethodColor(payment.paymentMethod) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {payment.createdAt}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2">
                      {payment.completedAt || '-'}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Box display="flex" gap={1}>
                      <Button
                        size="small"
                        startIcon={<Visibility />}
                        onClick={() => handlePaymentAction(payment, 'view')}
                      >
                        View
                      </Button>
                      <Button
                        size="small"
                        startIcon={<Receipt />}
                        onClick={() => handlePaymentAction(payment, 'receipt')}
                      >
                        Receipt
                      </Button>
                      {payment.status === 'pending' && (
                        <Button
                          size="small"
                          color="info"
                          startIcon={<Refresh />}
                          onClick={() => handlePaymentAction(payment, 'retry')}
                        >
                          Retry
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

      {filteredPayments.length === 0 && (
        <Box textAlign="center" sx={{ mt: 4 }}>
          <Typography variant="h6" color="textSecondary">
            No payments found matching the selected filter.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default SimplePayments;