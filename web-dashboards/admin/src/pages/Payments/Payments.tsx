import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Chip,
} from '@mui/material';
import {
  DataGrid,
  GridColDef,
} from '@mui/x-data-grid';

interface Payment {
  id: number;
  transaction_id: string;
  user_name: string;
  booking_id: string;
  amount: number;
  payment_method: string;
  status: string;
  created_at: string;
  razorpay_payment_id?: string;
}

const Payments: React.FC = () => {
  const [payments, setPayments] = useState<Payment[]>([]);

  useEffect(() => {
    const mockPayments: Payment[] = [
      {
        id: 1,
        transaction_id: 'TXN-001',
        user_name: 'John Doe',
        booking_id: 'BK-001',
        amount: 50,
        payment_method: 'razorpay',
        status: 'completed',
        created_at: '2024-01-15 10:30',
        razorpay_payment_id: 'pay_123456789',
      },
      {
        id: 2,
        transaction_id: 'TXN-002',
        user_name: 'Jane Smith',
        booking_id: 'BK-002',
        amount: 75,
        payment_method: 'razorpay',
        status: 'completed',
        created_at: '2024-01-14 15:20',
        razorpay_payment_id: 'pay_987654321',
      },
    ];
    setPayments(mockPayments);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'success';
      case 'pending': return 'warning';
      case 'failed': return 'error';
      case 'refunded': return 'info';
      default: return 'default';
    }
  };

  const columns: GridColDef[] = [
    { field: 'transaction_id', headerName: 'Transaction ID', width: 150 },
    { field: 'user_name', headerName: 'User', width: 150 },
    { field: 'booking_id', headerName: 'Booking ID', width: 120 },
    {
      field: 'amount',
      headerName: 'Amount',
      width: 120,
      renderCell: (params) => `₹${params.value}`,
    },
    { field: 'payment_method', headerName: 'Method', width: 120 },
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
    { field: 'razorpay_payment_id', headerName: 'Razorpay ID', width: 180 },
    { field: 'created_at', headerName: 'Date', width: 150 },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Payment Management
      </Typography>

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={payments}
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
    </Box>
  );
};

export default Payments;