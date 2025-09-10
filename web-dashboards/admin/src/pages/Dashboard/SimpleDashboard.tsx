import React from 'react';
import {
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
} from '@mui/material';
import {
  TrendingUp,
  People,
  Lock,
  LocalShipping,
  Payment,
  CheckCircle,
  Error,
} from '@mui/icons-material';

const SimpleDashboard: React.FC = () => {
  const stats = {
    totalUsers: 1250,
    totalLockers: 48,
    activeBookings: 23,
    totalRevenue: 45600,
    occupancyRate: 75,
    availableLockers: 12,
  };

  const recentActivity = [
    { id: 1, type: 'booking', message: 'New booking created by John Doe', time: '2 minutes ago', status: 'success' },
    { id: 2, type: 'payment', message: 'Payment received for booking #1234', time: '5 minutes ago', status: 'success' },
    { id: 3, type: 'locker', message: 'Locker L-15 opened successfully', time: '8 minutes ago', status: 'info' },
    { id: 4, type: 'error', message: 'Locker L-23 sensor malfunction', time: '12 minutes ago', status: 'error' },
    { id: 5, type: 'user', message: 'New user registration: Jane Smith', time: '15 minutes ago', status: 'success' },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success': return 'success';
      case 'error': return 'error';
      case 'info': return 'info';
      default: return 'default';
    }
  };

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'booking': return <LocalShipping />;
      case 'payment': return <Payment />;
      case 'locker': return <Lock />;
      case 'error': return <Error />;
      case 'user': return <People />;
      default: return <CheckCircle />;
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Smart Locker Dashboard
      </Typography>

      {/* Stats Cards */}
      <Box display="flex" flexWrap="wrap" gap={2} sx={{ mb: 3 }}>
        <Card sx={{ minWidth: 200, flex: 1 }}>
          <CardContent>
            <Box display="flex" alignItems="center">
              <People color="primary" sx={{ mr: 2 }} />
              <Box>
                <Typography color="textSecondary" gutterBottom>
                  Total Users
                </Typography>
                <Typography variant="h5">
                  {stats.totalUsers.toLocaleString()}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
        
        <Card sx={{ minWidth: 200, flex: 1 }}>
          <CardContent>
            <Box display="flex" alignItems="center">
              <Lock color="secondary" sx={{ mr: 2 }} />
              <Box>
                <Typography color="textSecondary" gutterBottom>
                  Total Lockers
                </Typography>
                <Typography variant="h5">
                  {stats.totalLockers}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
        
        <Card sx={{ minWidth: 200, flex: 1 }}>
          <CardContent>
            <Box display="flex" alignItems="center">
              <LocalShipping color="info" sx={{ mr: 2 }} />
              <Box>
                <Typography color="textSecondary" gutterBottom>
                  Active Bookings
                </Typography>
                <Typography variant="h5">
                  {stats.activeBookings}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
        
        <Card sx={{ minWidth: 200, flex: 1 }}>
          <CardContent>
            <Box display="flex" alignItems="center">
              <Payment color="success" sx={{ mr: 2 }} />
              <Box>
                <Typography color="textSecondary" gutterBottom>
                  Total Revenue
                </Typography>
                <Typography variant="h5">
                  ₹{stats.totalRevenue.toLocaleString()}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
        
        <Card sx={{ minWidth: 200, flex: 1 }}>
          <CardContent>
            <Box display="flex" alignItems="center">
              <TrendingUp color="warning" sx={{ mr: 2 }} />
              <Box>
                <Typography color="textSecondary" gutterBottom>
                  Occupancy Rate
                </Typography>
                <Typography variant="h5">
                  {stats.occupancyRate}%
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
        
        <Card sx={{ minWidth: 200, flex: 1 }}>
          <CardContent>
            <Box display="flex" alignItems="center">
              <CheckCircle color="success" sx={{ mr: 2 }} />
              <Box>
                <Typography color="textSecondary" gutterBottom>
                  Available Lockers
                </Typography>
                <Typography variant="h5">
                  {stats.availableLockers}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Recent Activity */}
      <Box display="flex" gap={3} flexWrap="wrap">
        <Paper sx={{ p: 2, flex: 1, minWidth: 400 }}>
          <Typography variant="h6" gutterBottom>
            Recent Activity
          </Typography>
          <List>
            {recentActivity.map((activity) => (
              <ListItem key={activity.id}>
                <ListItemIcon>
                  {getActivityIcon(activity.type)}
                </ListItemIcon>
                <ListItemText
                  primary={activity.message}
                  secondary={activity.time}
                />
                <Chip
                  label={activity.status}
                  color={getStatusColor(activity.status) as any}
                  size="small"
                />
              </ListItem>
            ))}
          </List>
        </Paper>

        <Paper sx={{ p: 2, flex: 1, minWidth: 300 }}>
          <Typography variant="h6" gutterBottom>
            System Status
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
              <Typography>Database Connection</Typography>
              <Chip label="Online" color="success" size="small" />
            </Box>
            <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
              <Typography>WhatsApp Service</Typography>
              <Chip label="Active" color="success" size="small" />
            </Box>
            <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
              <Typography>Payment Gateway</Typography>
              <Chip label="Connected" color="success" size="small" />
            </Box>
            <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
              <Typography>Hardware Status</Typography>
              <Chip label="2 Offline" color="warning" size="small" />
            </Box>
          </Box>
        </Paper>
      </Box>
    </Box>
  );
};

export default SimpleDashboard;