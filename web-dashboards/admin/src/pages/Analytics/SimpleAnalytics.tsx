import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Card,
  CardContent,
} from '@mui/material';
import {
  TrendingUp,
  People,
  Lock,
  Payment,
  LocalShipping,
  Schedule,
} from '@mui/icons-material';

const SimpleAnalytics: React.FC = () => {
  const analyticsData = {
    totalBookings: 1250,
    totalRevenue: 45600,
    averageBookingValue: 36.48,
    occupancyRate: 75,
    customerSatisfaction: 4.2,
    averageUsageTime: 18.5,
  };

  const monthlyData = [
    { month: 'Jan', bookings: 120, revenue: 4200 },
    { month: 'Feb', bookings: 150, revenue: 5100 },
    { month: 'Mar', bookings: 180, revenue: 6300 },
    { month: 'Apr', bookings: 200, revenue: 7200 },
    { month: 'May', bookings: 220, revenue: 7800 },
    { month: 'Jun', bookings: 250, revenue: 8900 },
  ];

  const lockerUsage = [
    { size: 'Small', usage: 45, color: '#2196f3' },
    { size: 'Medium', usage: 35, color: '#ff9800' },
    { size: 'Large', usage: 20, color: '#4caf50' },
  ];

  const itemTypes = [
    { type: 'Packages', count: 450, percentage: 45 },
    { type: 'Food', count: 300, percentage: 30 },
    { type: 'Documents', count: 150, percentage: 15 },
    { type: 'Laundry', count: 100, percentage: 10 },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Analytics Dashboard
      </Typography>

      {/* Key Metrics */}
      <Box display="flex" flexWrap="wrap" gap={2} sx={{ mb: 3 }}>
        <Card sx={{ minWidth: 200, flex: 1 }}>
          <CardContent>
            <Box display="flex" alignItems="center">
              <LocalShipping color="primary" sx={{ mr: 2 }} />
              <Box>
                <Typography color="textSecondary" gutterBottom>
                  Total Bookings
                </Typography>
                <Typography variant="h5">
                  {analyticsData.totalBookings.toLocaleString()}
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
                  ₹{analyticsData.totalRevenue.toLocaleString()}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ minWidth: 200, flex: 1 }}>
          <CardContent>
            <Box display="flex" alignItems="center">
              <TrendingUp color="info" sx={{ mr: 2 }} />
              <Box>
                <Typography color="textSecondary" gutterBottom>
                  Avg Booking Value
                </Typography>
                <Typography variant="h5">
                  ₹{analyticsData.averageBookingValue}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ minWidth: 200, flex: 1 }}>
          <CardContent>
            <Box display="flex" alignItems="center">
              <Lock color="warning" sx={{ mr: 2 }} />
              <Box>
                <Typography color="textSecondary" gutterBottom>
                  Occupancy Rate
                </Typography>
                <Typography variant="h5">
                  {analyticsData.occupancyRate}%
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ minWidth: 200, flex: 1 }}>
          <CardContent>
            <Box display="flex" alignItems="center">
              <People color="secondary" sx={{ mr: 2 }} />
              <Box>
                <Typography color="textSecondary" gutterBottom>
                  Customer Rating
                </Typography>
                <Typography variant="h5">
                  {analyticsData.customerSatisfaction}/5
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ minWidth: 200, flex: 1 }}>
          <CardContent>
            <Box display="flex" alignItems="center">
              <Schedule color="info" sx={{ mr: 2 }} />
              <Box>
                <Typography color="textSecondary" gutterBottom>
                  Avg Usage Time
                </Typography>
                <Typography variant="h5">
                  {analyticsData.averageUsageTime}h
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Box>

      <Box display="flex" flexWrap="wrap" gap={3}>
        {/* Monthly Trends */}
        <Paper sx={{ p: 3, flex: 2, minWidth: 400 }}>
          <Typography variant="h6" gutterBottom>
            Monthly Trends
          </Typography>
          <Box sx={{ mt: 2 }}>
            {monthlyData.map((data, index) => (
              <Box key={index} display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                <Typography variant="body1" sx={{ minWidth: 60 }}>
                  {data.month}
                </Typography>
                <Box display="flex" alignItems="center" sx={{ flex: 1, mx: 2 }}>
                  <Box
                    sx={{
                      height: 8,
                      backgroundColor: '#2196f3',
                      borderRadius: 4,
                      width: `${(data.bookings / 250) * 100}%`,
                      minWidth: 20,
                    }}
                  />
                </Box>
                <Typography variant="body2" sx={{ minWidth: 80 }}>
                  {data.bookings} bookings
                </Typography>
                <Typography variant="body2" sx={{ minWidth: 80, fontWeight: 'bold' }}>
                  ₹{data.revenue.toLocaleString()}
                </Typography>
              </Box>
            ))}
          </Box>
        </Paper>

        {/* Locker Size Usage */}
        <Paper sx={{ p: 3, flex: 1, minWidth: 300 }}>
          <Typography variant="h6" gutterBottom>
            Locker Size Usage
          </Typography>
          <Box sx={{ mt: 2 }}>
            {lockerUsage.map((data, index) => (
              <Box key={index} sx={{ mb: 3 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                  <Typography variant="body1">{data.size}</Typography>
                  <Typography variant="body2" fontWeight="bold">{data.usage}%</Typography>
                </Box>
                <Box
                  sx={{
                    height: 8,
                    backgroundColor: '#f0f0f0',
                    borderRadius: 4,
                    overflow: 'hidden',
                  }}
                >
                  <Box
                    sx={{
                      height: '100%',
                      backgroundColor: data.color,
                      width: `${data.usage}%`,
                      borderRadius: 4,
                    }}
                  />
                </Box>
              </Box>
            ))}
          </Box>
        </Paper>

        {/* Item Types Distribution */}
        <Paper sx={{ p: 3, flex: 1, minWidth: 300 }}>
          <Typography variant="h6" gutterBottom>
            Item Types Distribution
          </Typography>
          <Box sx={{ mt: 2 }}>
            {itemTypes.map((data, index) => (
              <Box key={index} display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                <Typography variant="body1">{data.type}</Typography>
                <Box display="flex" alignItems="center" gap={2}>
                  <Typography variant="body2">{data.count}</Typography>
                  <Typography variant="body2" color="textSecondary">
                    ({data.percentage}%)
                  </Typography>
                </Box>
              </Box>
            ))}
          </Box>
        </Paper>

        {/* Performance Metrics */}
        <Paper sx={{ p: 3, flex: 1, minWidth: 300 }}>
          <Typography variant="h6" gutterBottom>
            Performance Metrics
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
              <Typography>System Uptime</Typography>
              <Typography fontWeight="bold" color="success.main">99.8%</Typography>
            </Box>
            <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
              <Typography>Response Time</Typography>
              <Typography fontWeight="bold">1.2s</Typography>
            </Box>
            <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
              <Typography>Error Rate</Typography>
              <Typography fontWeight="bold" color="error.main">0.2%</Typography>
            </Box>
            <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
              <Typography>Active Users</Typography>
              <Typography fontWeight="bold">1,250</Typography>
            </Box>
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Typography>Peak Usage</Typography>
              <Typography fontWeight="bold">2-4 PM</Typography>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Box>
  );
};

export default SimpleAnalytics;